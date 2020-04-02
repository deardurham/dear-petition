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

from .constants import (
    JURISDICTION_CHOICES,
    DISTRICT_COURT,
    SUPERIOR_COURT,
    NOT_AVAILABLE,
    SEX_CHOICES,
    MALE,
    FEMALE,
    UNISEX
)


logger = logging.getLogger(__name__)

class CIPRSRecordManager(models.Manager):

    def create_record(self, batch, date_uploaded, report_pdf, label, data):
        '''Extract General, Case, and Defendant details from data 

        Parses the raw data from our JSONField (data) and
        places values in their associated model fields
        '''
        file_no = self.get_file_no(data)
        county = self.get_county(data)
        dob = self.get_dob(data)
        sex = self.get_sex(data)
        race = self.get_race(data)
        case_status = self.get_case_status(data)
        offense_date = self.get_offense_date(data)
        arrest_date = self.get_arrest_date(data)
        jurisdiction = self.get_jurisdiction(data)

        ciprs_record = self.create(
            batch=batch,
            date_uploaded=date_uploaded,
            report_pdf=report_pdf,
            label=label,
            data=data,
            file_no=file_no,
            county=county,
            dob=dob,
            sex=sex,
            race=race,
            case_status=case_status,
            offense_date=offense_date,
            arrest_date=arrest_date,
            jurisdiction=jurisdiction
        )
        return ciprs_record

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
    dob = models.DateField(null=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default=NOT_AVAILABLE)
    race = models.CharField(max_length=256, blank=True)
    case_status = models.CharField(max_length=256, blank=True)
    offense_date = models.DateTimeField(null=True)
    arrest_date = models.DateField(null=True)
    jurisdiction = models.CharField(
        max_length=16,
        choices=JURISDICTION_CHOICES,
        default=NOT_AVAILABLE
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
    
    def refresh_record(self):
        '''Updates model fields that depends on the data JSONField

        The record exists, but the raw data (data - JSONFIELD) has
        changed. Let's update the models that are extracting data
        from this field.
        '''
        record = CIPRSRecord.objects.get(pk=self.pk)
        record.file_no = self.get_file_no(self.data)
        record.county = self.get_county(self.data)
        record.dob = self.get_dob(self.data)
        record.sex = self.get_sex(self.data)
        record.race = self.get_race(self.data)
        record.case_status = self.get_case_status(self.data)
        record.offense_date = self.get_offense_date(self.data)
        record.arrest_date = self.get_arrest_date(self.data)
        record.jurisdiction = self.get_jurisdiction(self.data)
        
        
        return record.save(update_fields=[
            'file_no',
            'county',
            'dob',
            'sex',
            'race',
            'case_status',
            'offense_date',
            'arrest_date',
            'jurisdiction'
        ])

    def get_file_no(self, data):
        return data["General"].get("File No", "")

    def get_county(self, data):
        return data["General"].get("County", "")

    def get_dob(self, data):
        return data["Defendant"].get("Date of Birth/Estimated Age", "")
    
    def get_sex(self, data):
        return data["Defendant"].get("Sex", "")

    def get_race(self, data):
        return data["Defendant"].get("Race", "")

    def get_case_status(self, data):
        return data["Case Information"].get("Case Status", "")

    def get_offense_date(self, data):
        return data["Case Information"].get("Offense Date", "")

    def get_jurisdiction(self, data):
        is_superior = data["General"].get("Superior", "")
        is_district = data["General"].get("District", "")
        if is_superior:
            return SUPERIOR_COURT
        elif is_district:
            return DISTRICT_COURT
        else:
            return NOT_AVAILABLE

    def get_arrest_date(self, data):
        offense_date = data["Case Information"].get("Offense Date", "")
        return data["Offense Record"].get("Arrest Date", offense_date)
 

class Contact(models.Model):

    CONTACT_CATEGORIES = (("agency", "Agency"), ("attorney", "Attorney"))

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
            record = clean(record)
            for offense in record.offenses:
                yield (record, offense)

    def get_petition_offenses(self):
        petition_offenses = {}
        for i, (record, offense) in enumerate(self.offenses, 1):
            data = {}
            data["Fileno:" + str(i)] = {"V": record.file_no}
            data["ArrestDate:" + str(i)] = {"V": record.arrest_date}
            data["Description:" + str(i)] = {"V": offense.get("Description", "")}
            data["DOOF:" + str(i)] = {"V": record.offense_date}
            data["Disposition:" + str(i)] = {"V": record.disposition_method}
            data["DispositionDate:" + str(i)] = {"V": record.disposed_on}
            petition_offenses.update(data)
        return petition_offenses

    @property
    def most_recent_record(self):
        most_recent_record = None
        most_recent_offense_date = datetime(1900, 1, 1)
        for record in self.records.order_by("pk"):
            if not record.offense_date:
                continue
            offense_date = datetime.strptime(record.offense_date, "%Y-%m-%dT%H:%M:%S")
            if offense_date > most_recent_offense_date:
                most_recent_record = record
        if not most_recent_record:
            most_recent_record = self.records.order_by("pk").first()
        return most_recent_record
