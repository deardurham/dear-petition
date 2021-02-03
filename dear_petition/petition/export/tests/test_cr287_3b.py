import pytest

from django.utils import timezone

from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)
from dear_petition.petition.types import dismissed
from dear_petition.petition import constants

pytestmark = pytest.mark.django_db


def create_record(batch, jurisdiction, county):
    record = CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=jurisdiction,
        county=county,
    )
    guilty_offense = OffenseRecordFactory(
        action="CONVICTED",
        description="BREAK OR ENTER A MOTOR VEHICLE",
        severity="FELONY",
        offense=OffenseFactory(
            verdict="GUILTY",
            disposition_method="DISPOSED BY JUDGE",
            disposed_on=timezone.now(),
            ciprs_record=record,
            jurisdiction=jurisdiction,
        ),
    )
    OffenseRecordFactory(
        action="CHARGED",
        description="MISDEMEANOR LARCENY",
        severity="MISDEMEANOR",
        offense=OffenseFactory(
            disposed_on=timezone.now(),
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
            ciprs_record=record,
            jurisdiction=jurisdiction,
        ),
    )
    OffenseRecordFactory(
        action="CHARGED",
        description="POSS STOLEN GOODS/PROP",
        severity="MISDEMEANOR",
        offense=OffenseFactory(
            disposed_on=timezone.now(),
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
            ciprs_record=record,
            jurisdiction=jurisdiction,
        ),
    )
    return guilty_offense


@pytest.fixture
def durham_petition(batch):
    return PetitionFactory(
        batch=batch, county="DURHAM", jurisdiction=constants.DISTRICT_COURT
    )


@pytest.fixture
def durham_offense(durham_petition):
    return create_record(
        durham_petition.batch,
        jurisdiction=durham_petition.jurisdiction,
        county=durham_petition.county,
    )


def test_same_day_convictions(durham_offense, durham_petition):
    offenses = dismissed.same_day_convictions(durham_petition.get_all_offense_records())
    assert durham_offense in offenses
