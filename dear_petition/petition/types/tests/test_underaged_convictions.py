import pytest
from datetime import datetime

from django.utils import timezone

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)

pytestmark = pytest.mark.django_db


def test_underaged_conviction_included(batch, record1, non_dismissed_offense):
    record1.dob = datetime(2000, 1, 2)
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()
    offense_record = OffenseRecordFactory(
        action="CONVICTED", offense=non_dismissed_offense
    )
    assert offense_record in batch.underaged_conviction_records()


def test_overaged_conviction_not_included(batch, record1, non_dismissed_offense):
    record1.dob = datetime(2000, 1, 1)
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()
    offense_record = OffenseRecordFactory(
        action="CONVICTED", offense=non_dismissed_offense
    )
    assert offense_record not in batch.underaged_conviction_records()
