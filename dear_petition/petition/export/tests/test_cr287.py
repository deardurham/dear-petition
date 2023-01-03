import datetime as dt
import pytest

from dear_petition.petition import constants, utils
from dear_petition.petition.export.forms import AOCFormCR287


pytestmark = pytest.mark.django_db


@pytest.fixture
def form(petition_document, extra):
    return AOCFormCR287(petition_document, extra)


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


def test_map_petitioner__file_no(form, record2, offense_record1):
    form.map_file_no()
    assert form.data["ConsJdgmntFileNum"] == record2.file_no


#
# Petitioner
#


def test_map_petitioner__name(form):
    form.extra["name_petitioner"] = "Test Name"
    form.map_petitioner()
    assert form.data["NamePetitioner"] == form.extra["name_petitioner"]


def test_map_petitioner__race(form, record2, offense_record1):
    form.map_petitioner()
    assert form.data["Race"] == record2.race


def test_map_petitioner__sex(form, record2, offense_record1):
    form.map_petitioner()
    assert form.data["Sex"] == record2.sex


def test_map_petitioner__dob(form, record2, offense_record1):
    record2.dob = dt.date(2000, 1, 1)
    record2.save()
    form.map_petitioner()
    assert form.data["DOB"] == utils.format_petition_date(record2.dob)


def test_map_petitioner__address(form):
    form.extra["address1"] = "123 Test Pl."
    form.extra["address2"] = "Apt 404"
    form.map_petitioner()
    assert form.data["StreetAddr"] == form.extra["address1"]
    assert form.data["MailAddr"] == form.extra["address2"]


def test_map_petitioner__address2_empty(form):
    form.extra["address1"] = "123 Test Pl."
    form.extra["address2"] = ""
    form.map_petitioner()
    assert form.data["StreetAddr"] == form.extra["address1"]
    assert form.data["MailAddr"] == form.extra["address2"]


def test_map_petitioner__city(form):
    form.extra["city"] = "Test City"
    form.map_petitioner()
    assert form.data["City"] == form.extra["city"]


def test_map_petitioner__state(form):
    form.extra["state"] = constants.NORTH_CAROLINA
    form.map_petitioner()
    assert form.data["State"] == form.extra["state"]


def test_map_petitioner__zip_code(form):
    form.extra["zip_code"] = "27701"
    form.map_petitioner()
    assert form.data["ZipCode"] == form.extra["zip_code"]


#
# Attorney
#


def test_map_attorney__name(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["NameAtty"] == form.extra["attorney"].name


def test_map_attorney__street_address(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["StAddrAtty"] == form.extra["attorney"].address1


def test_map_attorney__mail_address(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["MailAddrAtty"] == form.extra["attorney"].address2


def test_map_attorney__city(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["CityAtty"] == form.extra["attorney"].city


def test_map_attorney__state(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["StateAtty"] == form.extra["attorney"].state


def test_map_attorney__zipcode(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["ZipCodeAtty"] == form.extra["attorney"].zipcode


def test_map_attorney__petition_not_filed_sign_name(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["PetitionNotFiledSignName"] == contact1.name


def test_map_attorney__petition_attorney_cbx(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["PetitionerAttorneyCbx"] == "Yes"


def test_map_attorney__petition_not_filed_sign_date(form, contact1):
    form.extra["attorney"] = contact1
    form.map_attorney()
    assert form.data["PetitionNotFiledSignDate"] == utils.format_petition_date(
        dt.datetime.today()
    )


#
# Agencies
#


def test_map_agencies__name(form, petition_document, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f"NameAgency{i}"
        if key in form.data:
            assert contact.name in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__street_address(form, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    addresses = [form.data[f"AddrAgency{i+1}"] for i in range(len(agencies))]
    for contact in agencies:
        assert contact.address1 in addresses


def test_map_agencies__mail_address(
    form, petition_document, contact1, contact2, contact3
):
    agencies = [contact1, contact2, contact3]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f"MailAgency{i}"
        if key in form.data:
            assert contact.address2 in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__city(form, petition_document, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f"CityAgency{i}"
        if key in form.data:
            assert contact.city in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__state(form, petition_document, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f'{"Stateagency" if i==2 else "StateAgency"}{i}'
        if key in form.data:
            assert contact.state in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__zipcode(form, petition_document, contact1, contact2, contact3):
    agencies = [contact1, contact2, contact3]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f"ZipAgency{i}"
        if key in form.data:
            assert contact.zipcode in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


#
# Offenses
#


def test_map_offenses__fileno(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["Fileno:1"] == record2.file_no


def test_map_offenses__arrest_date(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["ArrestDate:1"] == utils.format_petition_date(record2.arrest_date)


def test_map_offenses__description(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["Description:1"] == offense_record1.description


def test_map_offenses__offense_date(form, record2, offense_record1):
    form.map_offenses()
    assert form.data["DOOF:1"] == utils.format_petition_date(record2.offense_date)


def test_map_offenses__disposition_date(form, offense1, offense_record1):
    form.map_offenses()
    assert form.data["DismissalDate:1"] == utils.format_petition_date(
        offense1.disposed_on
    )
