import pytest

from dear_petition.petition import constants
from dear_petition.petition.export import mapper


pytestmark = pytest.mark.django_db


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
