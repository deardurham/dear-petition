import logging

from django.conf import settings

from dear_petition.petition.constants import (
    ATTACHMENT,
    DISMISSED,
    NOT_GUILTY,
    UNDERAGED_CONVICTIONS,
)
from dear_petition.petition import models as pm
from dear_petition.petition.etl.extract import parse_ciprs_document
from dear_petition.petition.types import (
    petition_offense_records,
    identify_distinct_petitions,
)


__all__ = ("import_ciprs_records",)

logger = logging.getLogger(__name__)


def import_ciprs_records(files, user, parser_mode, batch_label=""):
    """Import uploaded CIPRS records into models."""
    logger.info("Importing CIPRS records")
    if batch_label:
        batch, _ = pm.Batch.objects.get_or_create(user=user, label=batch_label)
    else:
        batch = pm.Batch.objects.create(user=user)
    logger.info(f"Created batch {batch.id}")
    for idx, file_ in enumerate(files):
        logger.info(f"Importing file {file_}")
        if settings.CIPRS_SAVE_PDF:
            batch_file = batch.files.create(file=file_)
            # Need to re-assign file_ since storages backend
            # closes file handle, so parse_ciprs_document below
            # fails
            file_ = batch_file.file
        for record_data in parse_ciprs_document(file_, parser_mode):
            record = pm.CIPRSRecord(batch=batch, data=record_data)
            record.refresh_record_from_data()
            if record.label and idx == 0 and not batch_label:
                batch.label = record.label
                batch.save()
    create_batch_petitions(batch)
    return batch


def create_batch_petitions(batch):
    # Dismissed
    create_petitions_from_records(batch, DISMISSED)
    # Not guilty
    create_petitions_from_records(batch, NOT_GUILTY)
    # Convictions
    create_petitions_from_records(batch, UNDERAGED_CONVICTIONS)
    # TODO: Misdemeanor


def create_petitions_from_records(batch, form_type):
    logger.info(f"Searching for {form_type} records (batch {batch})")
    record_set = petition_offense_records(batch, form_type)
    petition_types = identify_distinct_petitions(record_set)
    for petition_type in petition_types:
        petition = batch.petitions.create(
            form_type=form_type,
            jurisdiction=petition_type["jurisdiction"],
            county=petition_type["county"],
        )
        link_offense_records(petition)
        logger.info(
            f"Creating documents for {petition_type['county']} ({petition_type['jurisdiction']}) records"
        )
        create_documents(petition)
        logger.info(f"Associated {petition.offense_records.count()} total records")

        if form_type == UNDERAGED_CONVICTIONS:
            pm.PetitionOffenseRecord.objects.filter(petition_id=petition.id).update(
                active=False
            )


def link_offense_records(petition, filter_active=True):
    """Divide offense records across petition and any needed attachment forms."""

    offense_records = petition.get_all_offense_records()
    petition.offense_records.add(*offense_records)


def create_documents(petition):
    paginator = petition.get_offense_record_paginator()

    base_petition = pm.PetitionDocument.objects.create(petition=petition)
    base_petition.offense_records.add(*paginator.petition_offense_records())
    logger.info(
        f"Created {base_petition} with {base_petition.offense_records.count()} records"
    )

    previous_document = base_petition

    for attachment_records in paginator.attachment_offense_records():
        attachment = pm.PetitionDocument.objects.create(
            petition=petition, previous_document=previous_document
        )
        attachment.offense_records.add(*attachment_records)
        logger.info(
            f"Created {attachment} with {attachment.offense_records.count()} records"
        )
        previous_document = attachment
