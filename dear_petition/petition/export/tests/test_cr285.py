import pytest

from dear_petition.petition import constants, utils
from dear_petition.petition.etl.load import assign_agencies_to_documents
from dear_petition.petition.export.forms import AOCFormCR285
from dear_petition.petition.tests.factories import PetitionDocumentFactory
from dear_petition.petition.utils import get_285_form_agency_address


pytestmark = pytest.mark.django_db


@pytest.fixture
def attachment(batch, petition, petition_document, offense_record1):
    attachment_petition = PetitionDocumentFactory(
        petition=petition,
        previous_document=petition_document,
    )
    attachment_petition.offense_records.add(offense_record1)
    return attachment_petition


@pytest.fixture
def form(attachment, extra, client):
    form_extra = {}
    form_extra.update(extra)
    form_extra['client'] = client
    return AOCFormCR285(petition_document=attachment, extra=form_extra)


#
# Header
#


@pytest.mark.parametrize("county", ["DURHAM", "WAKE"])
def test_map_header__county(form, county):
    form.petition.county = county
    form.map_header()
    assert form.data["County"] == county


def test_map_header__superior(form):
    form.petition.jurisdiction = constants.SUPERIOR_COURT
    form.map_header()
    assert form.data["District"] == ""
    assert form.data["Superior"] == "Yes"


def test_map_header__district(form):
    form.petition.jurisdiction = constants.DISTRICT_COURT
    form.map_header()
    assert form.data["District"] == "Yes"
    assert form.data["Superior"] == ""


def test_map_petitioner__file_no(form):
    form.map_file_no()
    assert form.data["FileNo"] == form.MULTIPLE_FILE_NO_MSG


#
# Petitioner
#

def test_map_petitioner__name(form, client):
    form.map_petitioner()
    assert form.data["PetitionerName"] == client.name


#
# Agencies
#


def test_map_agencies__address(petition, form, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    addresses = [form.data[f"NameAddress{i+1}"] for i in range(len(agencies))]
    for agency in agencies:
        assert get_285_form_agency_address(agency) in addresses


#
# Offenses
#


def test_map_offenses__fileno(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["FileNoRow1"] == record2.file_no


def test_map_offenses__arrest_date(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["ArrestDateRow1"] == utils.format_petition_date(
        record2.arrest_date
    )


def test_map_offenses__description(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["OffenseDescRow1"] == offense_record1.description


def test_map_offenses__offense_date(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["DateOfOffenseRow1"] == utils.format_petition_date(
        record2.offense_date
    )


@pytest.mark.parametrize(
    "disposition_method",
    [
        "Dismissal without Leave by DA",
        "Dismissed by Court",
        "Deferred Prosecution Dismissal",
        "Discharge and Dismissal",
        "Conditional Discharge",
        "No Probable Cause",
        "Never To Be Served",
    ],
)
def test_map_offenses__disposition_method(
    form,
    offense1,
    offense_record1,
    disposition_method,
):
    offense1.disposition_method = disposition_method
    offense1.save()
    form.map_offenses()
    assert form.data["DispositionRow1"] == constants.DISPOSITION_METHOD_CODE_MAP.get(
        offense1.disposition_method.upper()
    )


def test_map_offenses__disposition_date(form, offense1, offense_record1):
    form.map_offenses()
    assert form.data["DispositionDateRow1"] == utils.format_petition_date(
        offense1.disposed_on
    )
