import pytest

from dear_petition.petition.tests.factories import (
    OffenseFactory,
    OffenseRecordFactory,
)
from dear_petition.petition.types import dismissed
from dear_petition.petition import constants

pytestmark = pytest.mark.django_db


@pytest.fixture
def guilty_bae(record1):
    offense = OffenseFactory(
        verdict="GUILTY",
        disposition_method="DISPOSED BY JUDGE",
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
    )
    return OffenseRecordFactory(
        action="CHARGED",
        description="BREAK OR ENTER A MOTOR VEHICLE",
        severity="FELONY",
        offense=offense,
    )


@pytest.fixture
def dismissed_larceny(record1, petition):
    offense = OffenseFactory(
        disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
    )
    record = OffenseRecordFactory(
        action="CHARGED",
        description="MISDEMEANOR LARCENY",
        severity="MISDEMEANOR",
        offense=offense,
    )
    record.petitions.add(petition)
    return record


@pytest.fixture
def dismissed_stolen_goods(record1, petition):
    offense = OffenseFactory(
        disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
    )
    record = OffenseRecordFactory(
        action="CHARGED",
        description="POSS STOLEN GOODS/PROP",
        severity="MISDEMEANOR",
        offense=offense,
    )
    record.petitions.add(petition)
    return record


def test_same_day_conviction(
    petition, guilty_bae, dismissed_larceny, dismissed_stolen_goods
):
    offenses = dismissed.same_day_conviction(petition.batch, petition.jurisdiction)
    assert guilty_bae in offenses
