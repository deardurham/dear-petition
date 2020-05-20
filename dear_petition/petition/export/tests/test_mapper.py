import pytest

from dear_petition.petition import constants
from dear_petition.petition.export import mapper
from dear_petition.petition.utils import make_datetime_aware

from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
)


pytestmark = pytest.mark.django_db

############################## map_petition test #########################
@pytest.mark.parametrize("county", ["DURHAM", "WAKE"])
def test_map_petition__county(petition, county):
    data = {}
    petition.county = county
    mapper.map_petition(data, petition)
    assert data["County"] == county


def test_map_petition__superior(petition):
    data = {}
    petition.jurisdiction = constants.SUPERIOR_COURT
    mapper.map_petition(data, petition)
    assert data["District"] == ""
    assert data["Superior"] == "Yes"


def test_map_petition__district(petition):
    data = {}
    petition.jurisdiction = constants.DISTRICT_COURT
    mapper.map_petition(data, petition)
    assert data["District"] == "Yes"
    assert data["Superior"] == ""


###################### map_petitioner tests #######################
def test_map_petitioner__name(petition):
    data = {}
    batch = BatchFactory()
    record = CIPRSRecordFactory(batch=batch)
    record.refresh_record_from_data()
    petition.batch = batch
    mapper.map_petitioner(data, petition)
    assert data["NamePetitioner"] == record.label


def test_map_petitioner__race(petition):
    data = {}
    batch = BatchFactory()
    record = CIPRSRecordFactory(batch=batch)
    record.refresh_record_from_data()
    petition.batch = batch
    mapper.map_petitioner(data, petition)
    assert data["Race"] == record.race


def test_map_petitioner__sex(petition):
    data = {}
    batch = BatchFactory()
    record = CIPRSRecordFactory(batch=batch)
    record.refresh_record_from_data()
    petition.batch = batch
    mapper.map_petitioner(data, petition)
    assert data["Sex"] == record.sex


def test_map_petitioner__ssn(petition):
    data = {}
    extra = {}
    extra["ssn"] = "000-000-0000"
    mapper.map_petitioner(data, petition, extra)
    assert data["SSN"] == extra["ssn"]


def test_map_petitioner__drivers_license(petition):
    data = {}
    extra = {}
    extra["drivers_license"] = "3429043204D"
    mapper.map_petitioner(data, petition, extra)
    assert data["DLNo"] == extra["drivers_license"]


def test_map_petitioner__dob(petition):
    data = {}
    batch = BatchFactory()
    record = CIPRSRecordFactory(batch=batch)
    record.refresh_record_from_data()
    petition.batch = batch
    mapper.map_petitioner(data, petition)
    assert data["DOB"] == make_datetime_aware(record.dob).date().strftime(
        constants.DATE_FORMAT
    )

    # def test_map_petitioner__age(petition):
    #     data = {}
    #     batch = BatchFactory()
    #     record = CIPRSRecordFactory(batch=batch)
    #     record.refresh_record_from_data()
    #     petition.batch = batch
    #     mapper.map_petitioner(data, petition)
    #     assert data["Age"] == record.age


def test_map_petitioner__file_no(petition):
    data = {}
    batch = BatchFactory()
    record = CIPRSRecordFactory(batch=batch)
    record.refresh_record_from_data()
    petition.batch = batch
    mapper.map_petitioner(data, petition)
    assert data["ConsJdgmntFileNum"] == record.file_no

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
