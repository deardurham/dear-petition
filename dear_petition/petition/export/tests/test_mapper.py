import pytest
import datetime as dt

from dear_petition.petition import constants
from dear_petition.petition.export import mapper
from dear_petition.petition.utils import make_datetime_aware, dt_obj_to_date

from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
)


pytestmark = pytest.mark.django_db

###################### map_petition test #########################
@pytest.mark.parametrize("county", ["DURHAM", "WAKE"])
def test_map_petition__county(data, petition, county):
    petition.county = county
    mapper.map_petition(data, petition)
    assert data["County"] == county


def test_map_petition__superior(data, petition):
    petition.jurisdiction = constants.SUPERIOR_COURT
    mapper.map_petition(data, petition)
    assert data["District"] == ""
    assert data["Superior"] == "Yes"


def test_map_petition__district(data, petition):
    petition.jurisdiction = constants.DISTRICT_COURT
    mapper.map_petition(data, petition)
    assert data["District"] == "Yes"
    assert data["Superior"] == ""


###################### map_petitioner tests #######################
# map_petitioner tests
def test_map_petitioner__name(data, petition, record1):
    mapper.map_petitioner(data, petition)
    assert data["NamePetitioner"] == record1.label


def test_map_petitioner__race(data, petition, record1):
    mapper.map_petitioner(data, petition)
    assert data["Race"] == record1.race


def test_map_petitioner__sex(data, petition, record1):
    mapper.map_petitioner(data, petition)
    assert data["Sex"] == record1.sex


def test_map_petitioner__dob(data, petition, record1):
    record1.dob = "2020-01-01"
    record1.save()
    mapper.map_petitioner(data, petition)
    assert data["DOB"] == make_datetime_aware(record1.dob).date().strftime(
        constants.DATE_FORMAT
    )


# def test_map_petitioner__age(data, petition, record1):
#     mapper.map_petitioner(data, petition)
#     assert data["Age"] == record1.age


def test_map_petitioner__file_no(data, petition, record1):
    mapper.map_petitioner(data, petition)
    assert data["ConsJdgmntFileNum"] == record1.file_no


def test_map_petitioner__ssn(data, petition, extra):
    extra["ssn"] = "000-000-0000"
    mapper.map_petitioner(data, petition, extra)
    assert data["SSN"] == extra["ssn"]


def test_map_petitioner__drivers_license(data, petition, extra):
    extra["drivers_license"] = "3429043204D"
    mapper.map_petitioner(data, petition, extra)
    assert data["DLNo"] == extra["drivers_license"]


def test_map_petitioner__drivers_license_state(data, petition, extra):
    extra["drivers_license_state"] = constants.NORTH_CAROLINA
    mapper.map_petitioner(data, petition, extra)
    assert data["DLState"] == extra["drivers_license_state"]


#################### map_attorney test ##################
def test_map_attorney__name(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["NameAtty"] == extra["attorney"].name


def test_map_attorney__street_address(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["StAddrAtty"] == extra["attorney"].address1


def test_map_attorney__mail_address(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["MailAddrAtty"] == extra["attorney"].address2


def test_map_attorney__city(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["CityAtty"] == extra["attorney"].city


def test_map_attorney__state(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["StateAtty"] == extra["attorney"].state


def test_map_attorney__zipcode(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["ZipCodeAtty"] == extra["attorney"].zipcode


def test_map_attorney__petition_not_filed_sign_name(petition, contact):
    data = {}
    extra = {}
    extra["attorney"] = contact
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionNotFiledSignName"] == contact.name


def test_map_attorney__petition_attorney_cbx(petition):
    data = {}
    extra = {}
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionerAttorneyCbx"] == "Yes"


def test_map_attorney__petition_not_filed_sign_date(petition):
    data = {}
    extra = {}
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionNotFiledSignDate"] == dt_obj_to_date(
        dt.datetime.today()
    ).strftime(constants.DATE_FORMAT)


############################## map_agencies test ####################


def test_map_agencies__name(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["NameAgency1"] == contact.name


def test_map_agencies__street_address(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["AddrAgency1"] == contact.address1


def test_map_agencies__mail_address(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["MailAgency1"] == contact.address2


def test_map_agencies__city(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["CityAgency1"] == contact.city


def test_map_agencies__state(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["StateAgency1"] == contact.state


def test_map_agencies__zipcode(petition, contact):
    data = {}
    extra = {}
    extra["agencies"] = [contact]
    mapper.map_agencies(data, petition, extra)
    assert data["ZipAgency1"] == contact.zipcode
