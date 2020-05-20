import pytest

from dear_petition.petition import constants
from dear_petition.petition.export import mapper
from dear_petition.petition.utils import make_datetime_aware

from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
)


pytestmark = pytest.mark.django_db

# map_petition test
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


# map_petitioner tests
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
