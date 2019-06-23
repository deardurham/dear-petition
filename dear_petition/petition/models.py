import json
import logging
import os
import subprocess
import tempfile
import ciprs_reader

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage
from django.db import models


logger = logging.getLogger(__name__)


class CIPRSRecord(models.Model):

    date_uploaded = models.DateTimeField(auto_now_add=True)
    report_pdf = models.FileField("Report PDF", upload_to='ciprs/', blank=True, null=True)
    label = models.CharField(max_length=2048, blank=True)
    data = JSONField(blank=True, null=True)

    def parse_report(self, report_pdf=None):
        """Save file locally, parse PDF, save to JSONField"""
        with tempfile.TemporaryDirectory(prefix='ciprs-') as tmp_folder:
            storage = FileSystemStorage(location=tmp_folder)
            storage.save('report.pdf', report_pdf)
            saved_file_path = os.path.join(storage.location, 'report.pdf')
            reader = ciprs_reader.PDFToTextReader(saved_file_path)
            try:
                reader.parse(source=settings.CIPRS_READER_SOURCE)
                data = json.loads(reader.json())
            except subprocess.CalledProcessError as e:
                logger.exception(e)
                data = {'error': str(e)}
            return data

    @property
    def file_no(self):
        return self.data['General'].get('File No', '')

    @property
    def county(self):
        return self.data['General'].get('County', '')

    @property
    def dob(self):
        return self.data['Defendant'].get('Date of Birth/Estimated Age', '')

    @property
    def case_status(self):
        return self.data['Case Information'].get('Case Status', '')

    @property
    def offense_date(self):
        return self.data['Case Information'].get('Offense Date', '')

    @property
    def disposed_on(self):
        return self.data['Offense Record'].get('Disposed On', '')

    @property
    def disposition_method(self):
        return self.data['Offense Record'].get('Disposition Method', '')
