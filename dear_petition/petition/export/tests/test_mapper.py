import pytest

from dear_petition.petition import constants
from dear_petition.petition.export import mapper


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "jurisdiction", [constants.DISTRICT_COURT, constants.SUPERIOR_COURT]
)
@pytest.mark.parametrize("county", ["DURHAM", "WAKE", "ORANGE"])
def test_map(petition, county, jurisdiction):
    data = {}
    petition.county = county
    petition.jurisdiction = jurisdiction
    mapper.map_petition(data, petition)
    assert {"County", "District", "Superior"} == data.keys()
    assert data["County"] == county
    if jurisdiction == constants.DISTRICT_COURT:
        assert data["District"] == "Yes"
        assert data["Superior"] == ""
    elif jurisdiction == constants.SUPERIOR_COURT:
        assert data["District"] == ""
        assert data["Superior"] == "Yes"
