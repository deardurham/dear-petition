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
