import datetime as dt
import pytest

from dear_petition.petition import constants, utils
from dear_petition.petition.export.forms import AOCFormCR287
from dear_petition.petition.tests.factories import AgencyFactory, ClientFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def form(petition_document, extra, client):
    form_extra = {"file_no": "Test File No"}
    form_extra.update(extra)
    form_extra["client"] = client
    return AOCFormCR287(petition_document, form_extra)


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


def test_map_file_no__filenum(form, record2, offense_record1):
    form.map_file_no()
    assert form.data["ConsJdgmntFileNum"] == form.extra["file_no"]


#
# Petitioner
#


def test_map_petitioner__name(form):
    client = ClientFactory(name="Test Name")
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["NamePetitioner"] == client.name


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
    client = ClientFactory(address1="123 Test St", address2="Apt 404")
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["StreetAddr"] == "123 Test St"
    assert form.data["MailAddr"] == "Apt 404"


def test_map_petitioner__address2_empty(form):
    client = ClientFactory(address1="123 Test Pl.", address2="")
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["StreetAddr"] == "123 Test Pl."
    assert form.data["MailAddr"] == ""


def test_map_petitioner__city(form):
    client = ClientFactory(city="Test City")
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["City"] == "Test City"


def test_map_petitioner__state(form):
    client = ClientFactory(state=constants.NORTH_CAROLINA)
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["State"] == constants.NORTH_CAROLINA


def test_map_petitioner__zip_code(form):
    client = ClientFactory(zipcode="27701")
    form.extra["client"] = client
    form.map_petitioner()
    assert form.data["ZipCode"] == "27701"


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


def test_map_agencies__name(form):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    names = [form.data[f"NameAgency{i+1}"] for i in range(len(agencies))]
    for contact in agencies:
        assert contact.name in names


def test_map_agencies__street_address(form):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    addresses = [form.data[f"AddrAgency{i+1}"] for i in range(len(agencies))]
    for contact in agencies:
        assert contact.address1 in addresses


def test_map_agencies__mail_address(form):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    mails = [form.data[f"MailAgency{i+1}"] for i in range(len(agencies))]
    for contact in agencies:
        assert contact.address2 in mails


def test_map_agencies__city(form, petition_document):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f"CityAgency{i}"
        if key in form.data:
            assert contact.city in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__state(form, petition_document):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    petition_document.agencies.set(agencies)
    form.map_agencies()
    for i, contact in enumerate(agencies, start=1):
        key = f'{"Stateagency" if i==2 else "StateAgency"}{i}'
        if key in form.data:
            assert contact.state in form.data[key]
        else:
            pytest.fail(f"Expected key '{key}' in form data")


def test_map_agencies__zipcode(form):
    agencies = [AgencyFactory(), AgencyFactory(), AgencyFactory()]
    form.petition_document.agencies.set(agencies)
    form.map_agencies()
    zips = [form.data[f"ZipAgency{i+1}"] for i in range(len(agencies))]
    for contact in agencies:
        assert contact.zipcode in zips


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


#
# Other
#


def test_checkmark_3b_no_checkmark(
    form,
):
    form.map_additional_forms()
    assert not form.data.get("ChargedA")
    assert not form.data.get("ChargedB")
    assert not form.data.get("ChargedDesc")
    assert not form.data.get("ChargedDescCont")


def test_checkmark_3b_checkmark_a_checked(
    form, petition_document, offense_record1, offense_record2
):
    form.map_additional_forms()
    assert form.data.get("ChargedA")
    assert not form.data.get("ChargedB")
    assert not form.data.get("ChargedDesc")
    assert not form.data.get("ChargedDescCont")


def test_checkmark_3b_checkmark_b_checked(form):
    form.petition_document.form_specific_data["is_checkmark_3b_checked"] = True
    form.petition_document.form_specific_data["charged_desc_string"] = "Test string"
    form.petition_document.form_specific_data[
        "charged_desc_cont_string"
    ] = "Test string (cont.)"
    form.map_additional_forms()
    assert not form.data.get("ChargedA")
    assert form.data.get("ChargedB")
    assert form.data.get("ChargedDesc")
    assert form.data.get("ChargedDescCont")
