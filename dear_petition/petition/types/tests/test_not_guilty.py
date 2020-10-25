import pytest

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)

pytestmark = pytest.mark.django_db


def test_charged_not_guilty_record(batch, not_guilty_offense):
    """Charged not guilty records should be included"""
    offense_record = OffenseRecordFactory(action="CHARGED", offense=not_guilty_offense)
    assert offense_record in batch.not_guilty_offense_records()


def test_non_charged_offense_record(batch, not_guilty_offense):
    """Non-charged records should be excluded."""
    offense_record = OffenseRecordFactory(
        action="CONVICTED", offense=not_guilty_offense
    )
    assert offense_record not in batch.dismissed_offense_records()


def test_non_not_guilty_verdict(batch, record1):
    offense = OffenseFactory(verdict="Guilty", ciprs_record=record1)
    offense_record = OffenseRecordFactory(action="CHARGED", offense=offense)
    assert offense_record not in batch.not_guilty_offense_records()


def test_not_both_dismissed_and_not_guilty(batch, record1):
    offense = OffenseFactory(
        disposition_method="DISMISSAL WITHOUT LEAVE BY DA",
        verdict="Not Guilty",
        ciprs_record=record1,
    )
    offense_record = OffenseRecordFactory(action="CHARGED", offense=offense)
    assert offense_record not in batch.not_guilty_offense_records(
        jurisdiction=record1.jurisdiction
    )


def test_petition_offenses(batch, record1, not_guilty_offense):
    """Petitions should return their own offense records."""
    offense_record = OffenseRecordFactory(action="CHARGED", offense=not_guilty_offense)
    petition = PetitionFactory(
        form_type=constants.NOT_GUILTY,
        jurisdiction=record1.jurisdiction,
        county=record1.county,
        batch=batch,
    )
    assert offense_record in petition.get_all_offense_records()
