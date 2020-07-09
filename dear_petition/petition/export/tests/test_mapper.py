import pytest
import datetime as dt

from dear_petition.petition import constants
from dear_petition.petition.export import mapper
from dear_petition.petition.utils import make_datetime_aware, dt_obj_to_date


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
    assert data["SNN"] == extra["ssn"]


def test_map_petitioner__drivers_license(data, petition, extra):
    extra["drivers_license"] = "3429043204D"
    mapper.map_petitioner(data, petition, extra)
    assert data["DLNo"] == extra["drivers_license"]


def test_map_petitioner__drivers_license_state(data, petition, extra):
    extra["drivers_license_state"] = constants.NORTH_CAROLINA
    mapper.map_petitioner(data, petition, extra)
    assert data["DLState"] == extra["drivers_license_state"]


#################### map_attorney test ##################
def test_map_attorney__name(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["NameAtty"] == extra["attorney"].name


def test_map_attorney__street_address(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["StAddrAtty"] == extra["attorney"].address1


def test_map_attorney__mail_address(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["MailAddrAtty"] == extra["attorney"].address2


def test_map_attorney__city(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["CityAtty"] == extra["attorney"].city


def test_map_attorney__state(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["StateAtty"] == extra["attorney"].state


def test_map_attorney__zipcode(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["ZipCodeAtty"] == extra["attorney"].zipcode


def test_map_attorney__petition_not_filed_sign_name(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionNotFiledSignName"] == contact1.name


def test_map_attorney__petition_attorney_cbx(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionerAttorneyCbx"] == "Yes"


def test_map_attorney__petition_not_filed_sign_date(data, petition, extra, contact1):
    extra["attorney"] = contact1
    mapper.map_attorney(data, petition, extra)
    assert data["PetitionNotFiledSignDate"] == dt_obj_to_date(
        dt.datetime.today()
    ).strftime(constants.DATE_FORMAT)


############################## map_agencies test ####################


def test_map_agencies__name(data, petition, extra, contact1, contact2, contact3):
    extra["agencies"] = [contact1, contact2, contact3]
    names = [contact.name for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_names = []
    for key, value in data.items():
        if "NameAgency" in key:
            data_names.append(value)
    for n in data_names:
        assert n in names


def test_map_agencies__street_address(
    data, petition, extra, contact1, contact2, contact3
):
    extra["agencies"] = [contact1, contact2, contact3]
    addresses = [contact.address1 for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_addresses = []
    for key, value in data.items():
        if "AddrAgency" in key:
            data_addresses.append(value)
    for a in data_addresses:
        assert a in addresses


def test_map_agencies__mail_address(
    data, petition, extra, contact1, contact2, contact3
):
    extra["agencies"] = [contact1, contact2, contact3]
    addresses = [contact.address2 for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_mail_addresses = []
    for key, value in data.items():
        if "MailAgency" in key:
            data_mail_addresses.append(value)
    for m in data_mail_addresses:
        assert m in addresses


def test_map_agencies__city(data, petition, extra, contact1, contact2, contact3):
    extra["agencies"] = [contact1, contact2, contact3]
    cities = [contact.city for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_cities = []
    for key, value in data.items():
        if "CityAgency" in key:
            data_cities.append(value)
    for c in data_cities:
        assert c in cities


def test_map_agencies__state(data, petition, extra, contact1, contact2, contact3):
    extra["agencies"] = [contact1, contact2, contact3]
    states = [contact.state for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_states = []
    for key, value in data.items():
        if "StateAgency" in key:
            data_states.append(value)
    for s in data_states:
        assert s in states


def test_map_agencies__zipcode(data, petition, extra, contact1, contact2, contact3):
    extra["agencies"] = [contact1, contact2, contact3]
    zipcodes = [contact.zipcode for contact in extra["agencies"]]
    mapper.map_agencies(data, petition, extra)
    data_zipcodes = []
    for key, value in data.items():
        if "ZipAgency" in key:
            data_zipcodes.append(value)
    for z in data_zipcodes:
        assert z in zipcodes


############################ map_offenses ################################
def test_map_offenses__fileno(data, petition, record2, offense1, offense_record1):
    mapper.map_offenses(data, petition)
    assert data["Fileno:1"] == record2.file_no


def test_map_offenses__arrest_date(data, petition, record2, offense1, offense_record1):
    mapper.map_offenses(data, petition)
    assert data["ArrestDate:1"] == record2.arrest_date.strftime(constants.DATE_FORMAT)


def test_map_offenses__description(data, petition, record2, offense1, offense_record1):
    mapper.map_offenses(data, petition)
    assert data["Description:1"] == offense_record1.description


def test_map_offenses__offense_date(data, petition, record2, offense1, offense_record1):
    mapper.map_offenses(data, petition)
    assert data["DOOF:1"] == record2.offense_date.strftime(constants.DATE_FORMAT)


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
    data, petition, record2, offense1, offense_record1, disposition_method,
):
    offense1.disposition_method = disposition_method
    offense1.save()
    mapper.map_offenses(data, petition)
    assert data["Disposition:1"] == constants.DISPOSITION_METHOD_CODE_MAP.get(
        offense1.disposition_method.upper()
    )


def test_map_offenses__disposition_date(
    data, petition, record2, offense1, offense_record1
):
    mapper.map_offenses(data, petition)
    assert data["DispositionDate:1"] == offense1.disposed_on.strftime(
        constants.DATE_FORMAT
    )
