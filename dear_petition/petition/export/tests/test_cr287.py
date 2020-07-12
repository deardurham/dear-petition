import datetime as dt
import pytest

from dear_petition.petition import constants, utils
from dear_petition.petition.export.forms import AOCFormCR287


pytestmark = pytest.mark.django_db


@pytest.fixture
def form(petition, extra):
    return AOCFormCR287(petition, extra)


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


#
# Petitioner
#


def test_map_petitioner__file_no(form, record1):
    form.map_petitioner()
    assert form.data["ConsJdgmntFileNum"] == record1.file_no


def test_map_petitioner__name(form, record1):
    form.map_petitioner()
    assert form.data["NamePetitioner"] == record1.label


def test_map_petitioner__race(form, record1):
    form.map_petitioner()
    assert form.data["Race"] == record1.race


def test_map_petitioner__sex(form, record1):
    form.map_petitioner()
    assert form.data["Sex"] == record1.sex


def test_map_petitioner__dob(form, record1):
    record1.dob = dt.date(2000, 1, 1)
    record1.save()
    form.map_petitioner()
    assert form.data["DOB"] == utils.format_petition_date(record1.dob)


def test_map_petitioner__ssn(form):
    form.extra["ssn"] = "000-000-0000"
    form.map_petitioner()
    assert form.data["SNN"] == form.extra["ssn"]


def test_map_petitioner__drivers_license(form):
    form.extra["drivers_license"] = "3429043204D"
    form.map_petitioner()
    assert form.data["DLNo"] == form.extra["drivers_license"]


def test_map_petitioner__drivers_license_state(form):
    form.extra["drivers_license_state"] = constants.NORTH_CAROLINA
    form.map_petitioner()
    assert form.data["DLState"] == form.extra["drivers_license_state"]


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


def test_map_agencies__name(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    names = [contact.name for contact in form.extra["agencies"]]
    form.map_agencies()
    data_names = []
    for key, value in form.data.items():
        if "NameAgency" in key:
            data_names.append(value)
    for n in data_names:
        assert n in names


def test_map_agencies__street_address(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    addresses = [contact.address1 for contact in form.extra["agencies"]]
    form.map_agencies()
    data_addresses = []
    for key, value in form.data.items():
        if "AddrAgency" in key:
            data_addresses.append(value)
    for a in data_addresses:
        assert a in addresses


def test_map_agencies__mail_address(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    addresses = [contact.address2 for contact in form.extra["agencies"]]
    form.map_agencies()
    data_mail_addresses = []
    for key, value in form.data.items():
        if "MailAgency" in key:
            data_mail_addresses.append(value)
    for m in data_mail_addresses:
        assert m in addresses


def test_map_agencies__city(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    cities = [contact.city for contact in form.extra["agencies"]]
    form.map_agencies()
    data_cities = []
    for key, value in form.data.items():
        if "CityAgency" in key:
            data_cities.append(value)
    for c in data_cities:
        assert c in cities


def test_map_agencies__state(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    states = [contact.state for contact in form.extra["agencies"]]
    form.map_agencies()
    data_states = []
    for key, value in form.data.items():
        if "StateAgency" in key:
            data_states.append(value)
    for s in data_states:
        assert s in states


def test_map_agencies__zipcode(form, contact1, contact2, contact3):
    form.extra["agencies"] = [contact1, contact2, contact3]
    zipcodes = [contact.zipcode for contact in form.extra["agencies"]]
    form.map_agencies()
    data_zipcodes = []
    for key, value in form.data.items():
        if "ZipAgency" in key:
            data_zipcodes.append(value)
    for z in data_zipcodes:
        assert z in zipcodes


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
    assert form.data["Disposition:1"] == constants.DISPOSITION_METHOD_CODE_MAP.get(
        offense1.disposition_method.upper()
    )


def test_map_offenses__disposition_date(form, offense1, offense_record1):
    form.map_offenses()
    assert form.data["DispositionDate:1"] == utils.format_petition_date(
        offense1.disposed_on
    )
