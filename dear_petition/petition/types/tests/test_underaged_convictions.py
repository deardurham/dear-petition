import pytest
from datetime import timedelta

from django.utils import timezone

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)

pytestmark = pytest.mark.django_db


def test_underaged_conviction(batch, record1, non_dismissed_offense):
    today = timezone.now()
    record1.dob = record1.offense_date.date() - timedelta(days=1)
    record1.save()
    offense_record = OffenseRecordFactory(
        action="CONVICTED", offense=non_dismissed_offense
    )
    assert offense_record in batch.underaged_conviction_records()
