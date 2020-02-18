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

import ciprs_reader
from dear_petition.petition.data_dict import clean
from dear_petition.users.models import User


logger = logging.getLogger(__name__)


class CIPRSRecord(models.Model):

    batch = models.ForeignKey("Batch", related_name="records", on_delete="CASCADE")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    report_pdf = models.FileField(
        "Report PDF", upload_to="ciprs/", blank=True, null=True
    )
    label = models.CharField(max_length=2048, blank=True)
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({self.pk})"

    class Meta:
        verbose_name = "CIPRSRecord"

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

    @property
    def file_no(self):
        return self.data["General"].get("File No", "")

    @property
    def county(self):
        return self.data["General"].get("County", "")

    @property
    def dob(self):
        return self.data["Defendant"].get("Date of Birth/Estimated Age", "")

    @property
    def case_status(self):
        return self.data["Case Information"].get("Case Status", "")

    @property
    def offense_date(self):
        return self.data["Case Information"].get("Offense Date", "")

    @property
    def arrest_date(self):
        return self.data["Offense Record"].get("Arrest Date", self.offense_date)

    @property
    def disposed_on(self):
        return self.data["Offense Record"].get("Disposed On", "")

    @property
    def disposition_method(self):
        return self.data["Offense Record"].get("Disposition Method", "")

    @property
    def district_court(self):
        return self.data["General"].get("District", "")

    @property
    def superior_court(self):
        return self.data["General"].get("Superior", "")

    @property
    def offenses(self):
        for offense in self.data["Offense Record"].get("Records", []):
            yield offense


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
        records = self.records.all()
        most_recent_record = records[0]
        most_recent_offense_date = most_recent_record.offense_date if most_recent_record.offense_date else datetime.min #The first record will just be returned if no other record has valid offense date
        for record in records[1:]:
            if not record.offense_date:
                logger.info(f"[most_recent_record] record pk={record.pk} does not have an offense date. Skipping.")
                continue
            try:
                offense_date = datetime.strptime(record.offense_date, "%Y-%m-%dT%H:%M:%S")
            except:
                logger.error(f"[most_recent_record] offense_date {record.offense_date} not in expected format, expecting %Y-%m-%dT%H:%M:%S")
            if offense_date > most_recent_offense_date:
                most_recent_record = record
        return most_recent_record
            

