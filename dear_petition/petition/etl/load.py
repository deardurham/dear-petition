import logging

from django.conf import settings
from django import forms

from dear_petition.petition.constants import DISMISSED
from dear_petition.petition.models import Batch, CIPRSRecord
from dear_petition.petition.etl.extract import parse_ciprs_document
from dear_petition.petition.types import identify_distinct_petitions


__all__ = ("import_ciprs_records",)

logger = logging.getLogger(__name__)


def import_ciprs_records(files, user):
    """Import uploaded CIPRS records into models."""
    logger.info("Importing CIPRS records")
    batch = Batch.objects.create(user=user)
    logger.info(f"Created batch {batch.id}")
    for idx, file_ in enumerate(files):
        logger.info(f"Importing file {file_}")
        for record_data in parse_ciprs_document(file_):
            record = CIPRSRecord(batch=batch, data=record_data)
            record.refresh_record_from_data()
            if settings.CIPRS_SAVE_PDF:
                record.report_pdf = file_
            if record.label and idx == 0:
                batch.label = record.label
                batch.save()
    create_batch_petitions(batch)
    return batch


def create_batch_petitions(batch):
    # Dismissed
    dismissed_records = batch.dismissed_offense_records()
    petition_types = identify_distinct_petitions(dismissed_records)
    for petition in petition_types:
        batch.petitions.create(
            form_type=DISMISSED,
            jurisdiction=petition["jurisdiction"],
            county=petition["county"],
        )
    # TODO: Not guilty
    # TODO: Misdemeanor
