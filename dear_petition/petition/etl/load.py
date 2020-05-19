import logging

from django.conf import settings
from django import forms

from dear_petition.petition.models import Batch, CIPRSRecord
from dear_petition.petition.etl.extract import parse_ciprs_document


__all__ = ("import_ciprs_records",)

logger = logging.getLogger(__name__)


def import_ciprs_records(files, user):
    """Import uploaded CIPRS records into models."""
    logger.info("Importing CIPRS records")
    batch = Batch.objects.create(user=user)
    logger.info(f"Created batch {batch.id}")
    for idx, file_ in enumerate(files):
        logger.info(f"Importing file {file_}")
        record = CIPRSRecord(batch=batch)
        if settings.CIPRS_SAVE_PDF:
            record.report_pdf = file_
        record.data = parse_ciprs_document(file_)
        if "error" in record.data:
            raise forms.ValidationError(record.data["error"])
        record.label = record.data.get("Defendant", {}).get("Name", "")
        if record.label and idx == 0:
            batch.label = record.label
            batch.save()
        record.refresh_record_from_data()
        batch.records.add(record)
    return batch
