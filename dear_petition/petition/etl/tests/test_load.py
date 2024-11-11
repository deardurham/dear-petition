import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import Batch
from dear_petition.petition.etl.load import (
    create_batch_petitions,
    import_ciprs_records,
    create_documents,
    assign_agencies_to_documents,
)
from dear_petition.petition.tests.factories import (
    ContactFactory,
    AgencyFactory,
    CIPRSRecordFactory,
    OffenseFactory,
    DismissedOffenseRecordFactory,
    PetitionOffenseRecordFactory,
)


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parser_mode", [1, 2])
def test_import_ciprs_records(fake_pdf, user, mock_ciprs_reader, parser_mode):
    """Test basic import_ciprs_records() without testing full ETL."""
    record = {"Defendant": {"Name": "Jon Doe"}}
    mock_ciprs_reader.return_value = [record]
    batch = import_ciprs_records([fake_pdf], user, parser_mode)
    assert Batch.objects.count() == 1
    assert batch.label == record["Defendant"]["Name"]
    assert batch.records.count() == 1


@pytest.mark.parametrize("parser_mode", [1, 2])
def test_import_ciprs_records_multi_files(
    fake_pdf, fake_pdf2, user, mock_ciprs_reader, parser_mode
):
    """Test basic import_ciprs_records() with multiple files without testing full ETL."""
    record1 = {"Defendant": {"Name": "Jon Doe"}, "General": {"File No": "00CR123456"}}
    record2 = {"Defendant": {"Name": "Jon Doe"}, "General": {"File No": "99CR123456"}}
    mock_ciprs_reader.side_effect = [[record1], [record2]]
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user, parser_mode)
    assert Batch.objects.count() == 1
    assert batch.label == record1["Defendant"]["Name"]
    assert batch.records.count() == 2


def test_created_petition(batch, record1, charged_dismissed_record, mock_ciprs_reader):
    """ETL should create identified generatable petitions."""
    create_batch_petitions(batch)
    petition = batch.petitions.first()
    assert petition.jurisdiction == record1.jurisdiction
    assert petition.county == record1.county


@pytest.mark.parametrize("parser_mode", [1, 2])
def test_save_pdf(fake_pdf, user, mock_transform_ciprs_document, parser_mode):
    record = [{"Defendant": {"Name": "Jon Doe"}}]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf], user, parser_mode)
    assert batch.files.count() == 1


@pytest.mark.parametrize("parser_mode", [1, 2])
def test_save_pdf__multiple(fake_pdf, fake_pdf2, user, mock_transform_ciprs_document, parser_mode):
    record = [{"Defendant": {"Name": "Jon Doe"}}]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user, parser_mode)
    assert batch.files.count() == 2


@pytest.mark.parametrize("parser_mode", [1, 2])
def test_save_pdf__duplicate(fake_pdf, fake_pdf2, user, mock_transform_ciprs_document, parser_mode):
    """
    Test that duplicate CIPRS records, both within the same file and in separate files, are not saved. In this case,
    the same CIPRS record (as determined by the file no) is uploaded twice in the first pdf file and twice in the second
    pdf file. It should not be saved all four times.  It should only be saved once.
    """
    record = [
        {"Defendant": {"Name": "Dee Fendant"}, "General": {"File No": "00CR123456"}},
        {"Defendant": {"Name": "Dee Fendant"}, "General": {"File No": "00CR123456"}},
    ]
    mock_transform_ciprs_document.return_value = record
    batch = import_ciprs_records([fake_pdf, fake_pdf2], user, parser_mode)
    assert batch.records.count() == 1


def test_assign_agencies_to_documents(petition, petition_document):
    contact1 = AgencyFactory()
    contact2 = AgencyFactory()
    contact3 = AgencyFactory()
    contact4 = AgencyFactory()

    petition.agencies.set([contact1, contact2, contact3])
    petition = assign_agencies_to_documents(petition)
    assert petition.documents.count() == 1

    # 4th contact should attachment
    petition.agencies.add(contact4)
    petition = assign_agencies_to_documents(petition)
    assert petition.documents.count() == 2


def test_removing_agency_does_not_delete_attachment_with_offense_records(
    petition, petition_document
):
    contact1 = AgencyFactory()
    contact2 = AgencyFactory()
    contact3 = AgencyFactory()
    contact4 = AgencyFactory()

    petition.agencies.set([contact1, contact2, contact3, contact4])
    ciprs_record = CIPRSRecordFactory(
        batch=petition.batch,
        jurisdiction=constants.DISTRICT_COURT,
        county=petition.county,
    )
    i = 0
    while i < 20:
        offense = OffenseFactory(
            ciprs_record=ciprs_record,
            disposition_method=constants.DISTRICT_COURT_WITHOUT_DA_LEAVE,
        )
        PetitionOffenseRecordFactory(
            petition=petition,
            offense_record=DismissedOffenseRecordFactory(offense=offense),
        )
        i += 1

    petition = create_documents(petition)
    petition = assign_agencies_to_documents(petition)
    assert petition.documents.count() == 2

    petition.agencies.remove(contact3)
    petition = assign_agencies_to_documents(petition)
    assert petition.documents.count() == 2
