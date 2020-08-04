import logging

from django.conf import settings

from dear_petition.petition.constants import ATTACHMENT, DISMISSED
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
        if settings.CIPRS_SAVE_PDF:
            batch_file = batch.files.create(file=file_)
            # Need to re-assign file_ since storages backend
            # closes file handle, so parse_ciprs_document below
            # fails
            file_ = batch_file.file
        for record_data in parse_ciprs_document(file_):
            record = CIPRSRecord(batch=batch, data=record_data)
            record.refresh_record_from_data()
            if record.label and idx == 0:
                batch.label = record.label
                batch.save()
    create_batch_petitions(batch)
    return batch


def create_batch_petitions(batch):
    # Dismissed
    dismissed_records = batch.dismissed_offense_records()
    petition_types = identify_distinct_petitions(dismissed_records)
    for petition_type in petition_types:
        petition = batch.petitions.create(
            form_type=DISMISSED,
            jurisdiction=petition_type["jurisdiction"],
            county=petition_type["county"],
        )
        link_offense_records_and_attachments(petition)
    # TODO: Not guilty
    # TODO: Misdemeanor


def link_offense_records_and_attachments(petition):
    """Divide offense records across petition and any needed attachment forms."""
    paginator = petition.get_offense_record_paginator()
    # add first 10 offense records to petition
    petition.offense_records.add(*paginator.petition_offense_records())
    # add offense records to attachment forms
    for attachment_records in paginator.attachment_offense_records():
        attachment = petition.attachments.create(
            batch=petition.batch,
            form_type=ATTACHMENT,
            jurisdiction=petition.jurisdiction,
            county=petition.county,
        )
        attachment.offense_records.add(*attachment_records)
