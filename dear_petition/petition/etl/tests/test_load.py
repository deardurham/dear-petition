import pytest

from dear_petition.petition.models import Batch
from dear_petition.petition.etl.load import import_ciprs_records


pytestmark = pytest.mark.django_db


def test_import_ciprs_records(fake_pdf, user, mock_ciprs_reader):
    """Test basic import_ciprs_records() without testing full ETL."""
    record = {"Defendant": {"Name": "Jon Doe"}}
    mock_ciprs_reader.return_value = record
    batch = import_ciprs_records([fake_pdf], user)
    assert Batch.objects.count() == 1
    assert batch.label == record["Defendant"]["Name"]
    assert batch.records.count() == 1


def test_import_ciprs_records_multi_files(fake_pdf, fake_pdf2, user, mock_ciprs_reader):
    """Test basic import_ciprs_records() with multiple files without testing full ETL."""
    record = {"Defendant": {"Name": "Jon Doe"}}
    mock_ciprs_reader.return_value = record
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user)
    assert Batch.objects.count() == 1
    assert batch.label == record["Defendant"]["Name"]
    assert batch.records.count() == 2
