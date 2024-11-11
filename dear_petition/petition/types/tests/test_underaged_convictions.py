import pytest
from datetime import datetime

from dear_petition.petition.tests.factories import (
    OffenseRecordFactory,
)

pytestmark = pytest.mark.django_db


def test_no_dob_conviction_not_included(batch, record1, non_dismissed_offense):
    # This tests the scenario where the record has no DOB (aka Portal), nor has the user added a DOB for the client.
    record1.dob = None
    record1.save()
    offense_record = OffenseRecordFactory(action="CONVICTED", offense=non_dismissed_offense)
    assert offense_record not in batch.underaged_conviction_records()


def test_underaged_conviction_included(batch, record1, non_dismissed_offense):
    record1.dob = datetime(2000, 1, 2)
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()
    offense_record = OffenseRecordFactory(action="CONVICTED", offense=non_dismissed_offense)
    assert offense_record in batch.underaged_conviction_records()


def test_overaged_conviction_not_included(batch, record1, non_dismissed_offense):
    record1.dob = datetime(2000, 1, 1)
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()
    offense_record = OffenseRecordFactory(action="CONVICTED", offense=non_dismissed_offense)
    assert offense_record not in batch.underaged_conviction_records()


def test_underaged_conviction_using_client_dob_included(batch, record1, non_dismissed_offense):
    # This tests the scenario where the record has no DOB (aka Portal), but the user has included a DOB for the client

    record1.dob = None
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()

    offense_record = OffenseRecordFactory(action="CONVICTED", offense=non_dismissed_offense)

    batch.client.dob = datetime(2000, 1, 2)
    batch.client.save()

    assert offense_record in batch.underaged_conviction_records()


def test_saving_client_dob_recalculates_underaged_convictions(
    batch, record1, non_dismissed_offense
):
    record1.dob = None
    record1.offense_date = datetime(2018, 1, 1)
    record1.save()

    offense_record = OffenseRecordFactory(action="CONVICTED", offense=non_dismissed_offense)

    batch.client.dob = datetime(2000, 1, 2)
    batch.client.save()

    assert offense_record in batch.underaged_conviction_records()

    batch.client.dob = datetime(2000, 1, 1)
    batch.client.save()

    assert offense_record not in batch.underaged_conviction_records()
