import json
import logging
import os
import subprocess
import tempfile
from collections import namedtuple
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import JSONField
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import IntegerField, Case, When, Value
from django.db.models.functions import Cast, Substr, Concat
from django.urls import reverse
from model_utils.models import TimeStampedModel
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

import ciprs_reader
from localflavor.us import us_states
from dear_petition.users.models import User
from dear_petition.users import constants as uc
from dear_petition.common.models import PrintableModelMixin
from . import constants as pc

from .constants import (
    JURISDICTION_CHOICES,
    DISTRICT_COURT,
    NOT_AVAILABLE,
    SEX_CHOICES,
    CONTACT_CATEGORIES,
    DATETIME_FORMAT,
    FORM_TYPES,
)

from .utils import make_datetime_aware


logger = logging.getLogger(__name__)


class CIPRSRecordManager(PrintableModelMixin, models.Manager):
    def create_record(self, batch, label, data):
        """Extract General, Case, and Defendant details from data

        Parses the raw data from our JSONField (data) and
        places values in their associated model fields.

        Note: This method is use to create the record that
        is why we are also passing batch, date_uploaded,
        report_pdf, and label alongside data. Although data is
        all that is needed when refresh_record_from_data is called.
        """
        ciprs_record = CIPRSRecord(batch=batch, label=label, data=data)
        ciprs_record.refresh_record_from_data()


class CIPRSRecord(PrintableModelMixin, models.Model):

    batch = models.ForeignKey("Batch", related_name="records", on_delete=models.CASCADE)
    batch_file = models.ForeignKey(
        "BatchFile",
        related_name="records",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=2048, blank=True)
    data = JSONField(blank=True, null=True)
    file_no = models.CharField(max_length=256, blank=True)
    county = models.CharField(max_length=256, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default=NOT_AVAILABLE)
    race = models.CharField(max_length=256, blank=True)
    case_status = models.CharField(max_length=256, blank=True)
    offense_date = models.DateTimeField(null=True, blank=True)
    arrest_date = models.DateField(null=True, blank=True)
    jurisdiction = models.CharField(
        max_length=16, choices=JURISDICTION_CHOICES, default=NOT_AVAILABLE
    )

    objects = CIPRSRecordManager()

    def __str__(self):
        return f"{self.label} {self.file_no} ({self.pk})"

    class Meta:
        verbose_name = "CIPRSRecord"

    def get_absolute_url(self):
        return reverse("view-record", kwargs={"pk": self.pk})

    def parse_report(self, report_pdf=None):
        """Save file locally, parse PDF, save to JSONField"""
        with tempfile.TemporaryDirectory(prefix="ciprs-") as tmp_folder:
            storage = FileSystemStorage(location=tmp_folder)
            storage.save("report.pdf", report_pdf)
            saved_file_path = os.path.join(storage.location, "report.pdf")
            reader = ciprs_reader.PDFToTextReader(saved_file_path)
            try:
                reader.parse(source=settings.CIPRS_READER_SOURCE)
                data = json.loads(reader.json())
            except subprocess.CalledProcessError as e:
                logger.exception(e)
                data = {"error": str(e)}
            return data

    def refresh_record_from_data(self):
        from dear_petition.petition.etl.refresh import refresh_record_from_data

        refresh_record_from_data(self)


class Offense(PrintableModelMixin, models.Model):
    ciprs_record = models.ForeignKey(
        "CIPRSRecord", related_name="offenses", on_delete=models.CASCADE
    )
    jurisdiction = models.CharField(
        choices=JURISDICTION_CHOICES, max_length=255, default=DISTRICT_COURT
    )
    disposed_on = models.DateField(blank=True, null=True)
    disposition_method = models.CharField(max_length=256)
    verdict = models.CharField(max_length=256, blank=True)
    plea = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.id} ({self.ciprs_record.file_no})"


class OffenseRecord(PrintableModelMixin, models.Model):
    offense = models.ForeignKey(
        "Offense", related_name="offense_records", on_delete=models.CASCADE
    )
    law = models.CharField(max_length=256, blank=True)
    code = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=256)
    severity = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

    def __str__(self):
        ciprs_record = self.offense.ciprs_record
        return f"{ciprs_record.file_no} {self.action} {self.severity} ({self.id})"

    @property
    def is_felony(self):
        return self.severity == "FELONY"

    @property
    def is_misdemeanor(self):
        return self.severity == "MISDEMEANOR"

    @property
    def county(self):
        return self.offense.ciprs_record.county

    @property
    def file_no(self):
        return self.offense.ciprs_record.file_no

    @property
    def disposed_on(self):
        return self.offense.disposed_on


class Contact(PrintableModelMixin, models.Model):
    name = models.CharField(max_length=512)
    category = models.CharField(
        max_length=16, choices=CONTACT_CATEGORIES, default="agency"
    )
    address1 = models.CharField("Address (Line 1)", max_length=512, blank=True)
    address2 = models.CharField("Address (Line 2)", max_length=512, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(choices=us_states.US_STATES, max_length=64, blank=True)
    zipcode = models.CharField("ZIP Code", max_length=16, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class Batch(PrintableModelMixin, models.Model):

    label = models.CharField(max_length=2048, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="batches", on_delete=models.CASCADE)
    emails = models.ManyToManyField(
        "sendgrid.Email", related_name="batches", blank=True
    )

    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.pk}: {self.label}"

    def get_absolute_url(self):
        return reverse("create-petition", kwargs={"pk": self.pk})

    @property
    def offenses(self):
        for record in self.records.all():
            o_records = record.offenses.first().offense_records.all()
            for offense in o_records:
                yield (record, offense)

    @property
    def most_recent_record(self):
        most_recent_record = None
        most_recent_offense_date = make_datetime_aware(
            datetime.min.strftime(DATETIME_FORMAT)
        )
        for record in self.records.order_by("pk"):
            if not record.offense_date:
                continue
            if record.offense_date > most_recent_offense_date:
                most_recent_record = record
        if not most_recent_record:
            most_recent_record = self.records.order_by("pk").first()
        return most_recent_record

    def petition_offense_records(self, petition_type, jurisdiction=""):
        from dear_petition.petition.types import petition_offense_records

        return petition_offense_records(self, petition_type, jurisdiction)

    def dismissed_offense_records(self, jurisdiction=""):
        return self.petition_offense_records(pc.DISMISSED, jurisdiction)

    def not_guilty_offense_records(self, jurisdiction=""):
        return self.petition_offense_records(pc.NOT_GUILTY, jurisdiction)

    def underaged_conviction_records(self, jurisdiction=""):
        return self.petition_offense_records(pc.UNDERAGED_CONVICTIONS, jurisdiction)

    @property
    def race(self):
        return self.records.first().race

    @property
    def sex(self):
        return self.records.first().sex

    @property
    def age(self):
        for record in self.records.all():
            dob = record.dob
            if dob:
                break
        if not dob:
            return
        today = timezone.now().date()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @property
    def automatic_delete_date(self):
        """Date when this batch will be automatically deleted by the cleanup task"""
        return self.date_uploaded + timedelta(
            hours=settings.CIPRS_RECORD_LIFETIME_HOURS
        )


def get_batch_file_upload_path(instance, filename):
    return "batch/%s/%s" % (instance.batch.id, filename)


class BatchFile(PrintableModelMixin, models.Model):
    batch = models.ForeignKey(Batch, related_name="files", on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_batch_file_upload_path)

    def __str__(self):
        return f"{self.file.name}"


class Comment(PrintableModelMixin, models.Model):

    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)
    text = models.TextField()
    batch = models.ForeignKey(Batch, related_name="comments", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        link = reverse(
            "create-petition", kwargs={"pk": self.batch.id, "tab": "comments"}
        )
        if self.user.is_staff:
            for staff_member in User.objects.filter(is_staff=True):
                staff_member.send_email(
                    subject=pc.NEW_COMMENT_EMAIL_SUBJECT,
                    message=pc.NEW_COMMENT_EMAIL_MESSAGE.format(
                        batch=self.batch.id,
                        user=staff_member.name,
                        text=self.text,
                        link=link,
                    ),
                )
        super(Comment, self).save(*args, **kwargs)


class Petition(PrintableModelMixin, TimeStampedModel):

    form_type = models.CharField(choices=FORM_TYPES, max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="petitions")
    county = models.CharField(max_length=256, blank=True)
    jurisdiction = models.CharField(choices=JURISDICTION_CHOICES, max_length=255)
    offense_records = models.ManyToManyField(
        OffenseRecord, related_name="petitions", through="PetitionOffenseRecord"
    )
    agencies = models.ManyToManyField(Contact, related_name="+")

    def __str__(self):
        return f"{self.form_type} {self.get_jurisdiction_display()} in {self.county}"

    def get_offense_record_paginator(self, filter_active=True):
        from dear_petition.petition.etl.paginator import OffenseRecordPaginator

        return OffenseRecordPaginator(self, filter_active=filter_active)

    def get_all_offense_records(self, include_annotations=True, filter_active=False):
        """
        Return all (nonpaginated) offenses for this petition type, jurisdiction, and
        county. This is typically only used at the end of the ETL process to divide
        offense records across any needed attachment forms.

        Post-ETL usage should just use the offense_records ManyToManyField.
        """
        two_digit_current_year = timezone.now().year % 2000  # Returns 21 given 2021

        qs = self.batch.petition_offense_records(
            petition_type=self.form_type, jurisdiction=self.jurisdiction
        ).select_related("offense__ciprs_record")
        qs = qs.filter(
            offense__ciprs_record__county=self.county,
        )

        if filter_active:
            qs = qs.filter(petitionoffenserecord__active=True)

        if include_annotations:
            qs = (
                qs.annotate(
                    first_two_digits_file_number_chars=Substr(
                        "offense__ciprs_record__file_no", 1, 2
                    )
                )
                .annotate(
                    first_two_digits_file_number=Cast(
                        "first_two_digits_file_number_chars",
                        output_field=IntegerField(),
                    )
                )
                .annotate(
                    file_number_year=Case(
                        When(
                            first_two_digits_file_number__gt=two_digit_current_year,
                            then=Concat(
                                Value("19"), "first_two_digits_file_number_chars"
                            ),
                        ),
                        When(
                            first_two_digits_file_number__lte=two_digit_current_year,
                            then=Concat(
                                Value("20"), "first_two_digits_file_number_chars"
                            ),
                        ),
                    )
                )
                .order_by(
                    "file_number_year",
                    "offense__ciprs_record__file_no",
                    "pk",
                )
            )

        return qs

    @property
    def base_document(self):
        return self.documents.get(previous_document__isnull=True)

    def has_attachments(self):
        return self.documents.count() > 1


# Look-alike Petition object used to support JSON data-driven petitions
DataPetition = namedtuple("DataPetition", ["form_type", "data_only"], defaults=[True])
DataPetitionDocument = namedtuple("DataPetitionDocument", ["petition"])


class PetitionDocument(PrintableModelMixin, models.Model):
    petition = models.ForeignKey(
        Petition, on_delete=models.CASCADE, related_name="documents"
    )
    offense_records = models.ManyToManyField(OffenseRecord, related_name="documents")
    previous_document = models.OneToOneField(
        "self", on_delete=models.CASCADE, null=True, related_name="following_document"
    )
    agencies = models.ManyToManyField(Contact, related_name="+")

    @property
    def is_attachment(self):
        return self.previous_document is not None

    @property
    def form_type(self):
        if self.previous_document_id:
            return pc.ATTACHMENT
        else:
            return self.petition.form_type

    @property
    def jurisdiction(self):
        return self.petition.jurisdiction

    @property
    def county(self):
        return self.petition.county

    def __str__(self):
        attachment = " attachment " if self.is_attachment else " "
        jurisdiction = self.petition.get_jurisdiction_display()
        return f"{self.county} {self.form_type} {jurisdiction}{attachment}({self.id})"


class PetitionOffenseRecord(PrintableModelMixin, models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    offense_record = models.ForeignKey(OffenseRecord, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


class GeneratedPetition(PrintableModelMixin, TimeStampedModel):
    username = models.CharField(max_length=uc.NAME_MAX_LENGTH)
    form_type = models.CharField(choices=FORM_TYPES, max_length=255)
    number_of_charges = models.IntegerField()
    batch_id = models.PositiveIntegerField()
    county = models.CharField(max_length=256, blank=True, null=True)
    jurisdiction = models.CharField(
        choices=JURISDICTION_CHOICES, max_length=255, null=True
    )
    race = models.CharField(max_length=256, null=True)
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, default=NOT_AVAILABLE, null=True
    )
    age = models.PositiveIntegerField(null=True)

    @classmethod
    def get_stats_generated_petition(cls, petition_document_id, user):
        petition_document = PetitionDocument.objects.get(id=petition_document_id)
        batch = petition_document.petition.batch
        user = user

        generated_petition = GeneratedPetition.objects.create(
            username=user.username,
            form_type=petition_document.form_type,
            number_of_charges=petition_document.offense_records.count(),
            batch_id=batch.id,
            county=petition_document.county,
            jurisdiction=petition_document.jurisdiction,
            race=batch.race,
            sex=batch.sex,
            age=batch.age,
        )

        user.last_generated_petition_time = timezone.now()
        user.save()

        return generated_petition
