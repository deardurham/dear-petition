import json
import logging
import tempfile
import subprocess

from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage
from django.db import models


logger = logging.getLogger(__name__)


class CIPRSRecord(models.Model):

    date_uploaded = models.DateTimeField(auto_now_add=True)
    report_pdf = models.FileField("Report PDF", upload_to='ciprs/')
    label = models.CharField(max_length=2048, blank=True)
    data = JSONField(blank=True, null=True)

    def parse_report(self):
        """Save file locally, parse PDF, save to JSONField"""
        with tempfile.TemporaryDirectory(prefix='ciprs-') as tmp_folder:
            storage = FileSystemStorage(location=tmp_folder)
            storage.save('record.pdf', record.report_pdf)
            saved_file_path = os.path.join(storage.location, 'record.pdf')
            reader = ciprs_reader.PDFToTextReader(saved_file_path)
            try:
                reader.parse()
                record.data = json.loads(reader.json())
            except subprocess.CalledProcessError as e:
                logger.exception(e)
                record.data = {'error': str(e)}
            finally:
                record.save()
