import pytest

from dear_petition.petition import constants, utils
from dear_petition.petition.export.forms import AOCFormCR285
from dear_petition.petition.tests.factories import PetitionFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def attachment(batch, petition, offense_record1):
    attachment_petition = PetitionFactory(
        batch=batch, parent=petition, form_type=constants.ATTACHMENT
    )
    attachment_petition.offense_records.add(offense_record1)
    return attachment_petition


@pytest.fixture
def form(attachment, extra):
    return AOCFormCR285(petition=attachment, extra=extra)


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
    form.jurisdiction = constants.DISTRICT_COURT
    form.map_header()
    assert form.data["District"] == "Yes"
    assert form.data["Superior"] == ""


def test_map_petitioner__file_no(form):
    form.map_file_no()
    assert form.data["FileNo"] == form.MULTIPLE_FILE_NO_MSG


#
# Petitioner
#


def test_map_petitioner__name(form, record2, offense_record1):
    form.map_petitioner()
    assert form.data["PetitionerName"] == record2.label


#
# Agencies
#


@pytest.mark.parametrize(
    "field", ["name", "address1", "address2", "city", "state", "zipcode"],
)
def test_map_agencies__fields(field, form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    form.map_agencies()
    for i, agency in enumerate(form.extra["agencies"], 1):
        assert getattr(agency, field) in form.data[f"NameAddress{i}"]


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
    form, offense1, offense_record1, disposition_method,
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
