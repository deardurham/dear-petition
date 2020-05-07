import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

import ciprs_reader
from dear_petition.petition.data_dict import clean
from dear_petition.users.models import User
from . import constants as pc

from .constants import (
    JURISDICTION_CHOICES,
    DISTRICT_COURT,
    SUPERIOR_COURT,
    NOT_AVAILABLE,
    SEX_CHOICES,
    MALE,
    FEMALE,
    UNKNOWN,
    CONTACT_CATEGORIES,
    DATETIME_FORMAT,
    DATE_FORMAT,
    CHARGED,
    FORM_TYPES,
)

from .utils import (
    dt_obj_to_date,
    make_datetime_aware,
)


logger = logging.getLogger(__name__)


class CIPRSRecordManager(models.Manager):
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


class CIPRSRecord(models.Model):

    batch = models.ForeignKey("Batch", related_name="records", on_delete="CASCADE")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    report_pdf = models.FileField(
        "Report PDF", upload_to="ciprs/", blank=True, null=True
    )
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
        return f"{self.label} ({self.pk})"

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
        """Updates model fields that depends on the data JSONField

        The record exists, but the raw data (data - JSONFIELD) has
        changed. Let's update the models that are extracting data
        from this field.
        """
        self.file_no = (
            self.data.get("General", {}).get("File No", "") if self.data else ""
        )
        self.county = (
            self.data.get("General", {}).get("County", "") if self.data else ""
        )
        self.dob = (
            self.data.get("Defendant", {}).get("Date of Birth/Estimated Age", None)
            if self.data
            else None
        )
        self.sex = (
            self.data.get("Defendant", {}).get("Sex", NOT_AVAILABLE)
            if self.data
            else NOT_AVAILABLE
        )
        self.race = self.data.get("Defendant", {}).get("Race", "") if self.data else ""
        self.case_status = (
            self.data.get("Case Information", {}).get("Case Status", "")
            if self.data
            else ""
        )
        self.offense_date = (
            make_datetime_aware(
                self.data.get("Case Information", {}).get("Offense Date", None)
            )
            if self.data
            else None
        )
        self.arrest_date = (
            self.data.get("Offense Record", {}).get(
                "Arrest Date", dt_obj_to_date(self.offense_date)
            )
            if self.data
            else None
        )
        self.jurisdiction = self.get_jurisdiction()
        self.save()
        # Record has been saved, now let's update the offense data.
        # we are using the get_or_create queryset method.
        # based upon the kwargs we are passing, either a object will
        # be retrieved from the db or the object will be created.
        # Alternatively we could use update_or_create method, but since
        # we are only getting this data by reading the pdf, I think
        # get_or_create is more suitable. Essentially, we are just
        # checking whether the defendant has more offenses since the last
        # time we ran this method. If a additional offenses are found add
        # the offense. If a UI interface is added that allows lawyers to
        # make changes to a users a offenses (I doubt it) then we need
        # think about revising the methods chosen here.
        offenses = self.data.get("Offense Record", {})

        # Check and remove any existing Offense Records and the existing Offenses
        # before reading from raw_data
        existing_offense_records = OffenseRecord.objects.filter(
            offense__ciprs_record=self
        )
        existing_offenses = Offense.objects.filter(ciprs_record=self)
        existing_offense_records.delete()
        existing_offenses.delete()
        if offenses:
            offense, created = Offense.objects.get_or_create(
                ciprs_record=self,
                disposed_on=offenses.get("Disposed On", None),
                disposition_method=offenses.get("Disposition Method", ""),
            )
            offense_records = offenses.get("Records", [])
            for offense_record in offense_records:
                try:
                    code = int(offense_record.get("Code"))
                except ValueError:
                    code = None
                OffenseRecord.objects.create(
                    offense=offense,
                    law=offense_record.get("Law", ""),
                    code=code,
                    action=offense_record.get("Action", ""),
                    severity=offense_record.get("Severity", ""),
                    description=offense_record.get("Description", ""),
                )

    def get_jurisdiction(self):
        if self.data:
            is_superior = self.data.get("General", {}).get("Superior", "")
            is_district = self.data.get("General", {}).get("District", "")
            if is_superior:
                return SUPERIOR_COURT
            elif is_district:
                return DISTRICT_COURT
            else:
                return NOT_AVAILABLE
        return NOT_AVAILABLE


class Offense(models.Model):
    ciprs_record = models.ForeignKey(
        "CIPRSRecord", related_name="offenses", on_delete="CASCADE"
    )
    disposed_on = models.DateField(blank=True, null=True)
    disposition_method = models.CharField(max_length=256)

    def __str__(self):
        return f"offense ${self.pk}"


class OffenseRecord(models.Model):
    offense = models.ForeignKey(
        "Offense", related_name="offense_records", on_delete="CASCADE"
    )
    law = models.CharField(max_length=256, blank=True)
    code = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=256)
    severity = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f"offense record {self.pk}"


class Contact(models.Model):
    name = models.CharField(max_length=512)
    category = models.CharField(
        max_length=16, choices=CONTACT_CATEGORIES, default="agency"
    )
    address1 = models.CharField("Address (Line 1)", max_length=512, blank=True)
    address2 = models.CharField("Address (Line 2)", max_length=512, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zipcode = models.CharField("ZIP Code", max_length=16, blank=True)

    def __str__(self):
        return self.name


class Batch(models.Model):

    label = models.CharField(max_length=2048, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="batches", on_delete="CASCADE")

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

    def get_petition_offenses(self):
        # Only Charged Offenses should be shown on the generated petition
        charged_offenses = [
            (record, offense)
            for (record, offense) in self.offenses
            if offense.action == CHARGED
        ]
        petition_offenses = {}
        for i, (record, offense) in enumerate(charged_offenses, 1):
            # The index of the offense determines what line on the petition form
            # the offense will be on
            formatted_arrest_date = (
                record.arrest_date.strftime(DATE_FORMAT) if record.arrest_date else ""
            )
            formatted_offense_date = (
                record.offense_date.strftime(DATE_FORMAT) if record.offense_date else ""
            )
            formatted_disposed_on = (
                record.offenses.first().disposed_on.strftime(DATE_FORMAT)
                if record.offenses.first().disposed_on
                else ""
            )
            data = {}
            data["Fileno:" + str(i)] = {"V": record.file_no}
            data["ArrestDate:" + str(i)] = {"V": formatted_arrest_date}
            data["Description:" + str(i)] = {"V": offense.description}
            data["DOOF:" + str(i)] = {"V": formatted_offense_date}
            data["Disposition:" + str(i)] = {
                "V": record.offenses.first().disposition_method
            }
            data["DispositionDate:" + str(i)] = {"V": formatted_disposed_on}
            petition_offenses.update(data)
        return petition_offenses

    @property
    def most_recent_record(self):
        most_recent_record = None
        most_recent_offense_date = make_datetime_aware(
            datetime(1900, 1, 1).strftime(DATETIME_FORMAT)
        )
        for record in self.records.order_by("pk"):
            if not record.offense_date:
                continue
            if record.offense_date > most_recent_offense_date:
                most_recent_record = record
        if not most_recent_record:
            most_recent_record = self.records.order_by("pk").first()
        return most_recent_record


class Comment(models.Model):

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


# Inputs
#
#
#
#


class Petition(models.Model):

    form_type = models.CharField(choices=FORM_TYPES, max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="petitions")
    county = models.CharField(max_length=255)
    jurisdiction = models.CharField(choices=JURISDICTION_CHOICES, max_length=255)
