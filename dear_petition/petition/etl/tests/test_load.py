import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import Batch
from dear_petition.petition.etl.load import (
    create_batch_petitions,
    import_ciprs_records,
)


pytestmark = pytest.mark.django_db


def test_import_ciprs_records(fake_pdf, user, mock_ciprs_reader):
    """Test basic import_ciprs_records() without testing full ETL."""
    record = {"Defendant": {"Name": "Jon Doe"}}
    mock_ciprs_reader.return_value = [record]
    batch = import_ciprs_records([fake_pdf], user)
    assert Batch.objects.count() == 1
    assert batch.label == record["Defendant"]["Name"]
    assert batch.records.count() == 1


def test_import_ciprs_records_multi_files(fake_pdf, fake_pdf2, user, mock_ciprs_reader):
    """Test basic import_ciprs_records() with multiple files without testing full ETL."""
    record = {"Defendant": {"Name": "Jon Doe"}}
    mock_ciprs_reader.return_value = [record]
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user)
    assert Batch.objects.count() == 1
    assert batch.label == record["Defendant"]["Name"]
    assert batch.records.count() == 2


def test_created_petition(batch, record1, charged_dismissed_record, mock_ciprs_reader):
    """ETL should created identified generatable petitions."""
    create_batch_petitions(batch)
    petition = batch.petitions.first()
    assert petition.jurisdiction == record1.jurisdiction
    assert petition.county == record1.county


def test_dont_save_pdf(fake_pdf, user, settings, mock_transform_ciprs_document):
    settings.CIPRS_SAVE_PDF = False
    record = [{"Defendant": {"Name": "Jon Doe"}}]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf], user)
    assert not batch.files.exists()


def test_save_pdf(fake_pdf, user, settings, mock_transform_ciprs_document):
    settings.CIPRS_SAVE_PDF = True
    record = [{"Defendant": {"Name": "Jon Doe"}}]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf], user)
    assert batch.files.count() == 1


def test_save_pdf__multiple(
    fake_pdf, fake_pdf2, user, settings, mock_transform_ciprs_document
):
    settings.CIPRS_SAVE_PDF = True
    record = [{"Defendant": {"Name": "Jon Doe"}}]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user)
    assert batch.files.count() == 2
