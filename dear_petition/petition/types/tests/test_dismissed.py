import pytest

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("method", constants.DISMISSED_DISPOSITION_METHODS)
def test_charged_disposition_methods(batch, record1, method):
    """CHARGED offense records should be included for all dismissed disposition methods."""
    offense = OffenseFactory(disposition_method=method, ciprs_record=record1)
    offense_record = OffenseRecordFactory(action="CHARGED", offense=offense)
    assert offense_record in batch.dismissed_offense_records()


def test_non_charged_offense_record(batch, dismissed_offense):
    """Non-CHARGED dismissed offense records should be excluded."""
    offense_record = OffenseRecordFactory(action="CONVICTED", offense=dismissed_offense)
    assert offense_record not in batch.dismissed_offense_records()


def test_non_dismissed_disposition_method(batch, non_dismissed_offense):
    """Offenses with non-dismissed disposition methods should be excluded."""
    offense_record = OffenseRecordFactory(
        action="CHARGED", offense=non_dismissed_offense
    )
    assert offense_record not in batch.dismissed_offense_records()


def test_infraction_severity_offense_record(batch, dismissed_offense):
    """Offense records with severity INFRACTION should be excluded."""
    infraction_record = OffenseRecordFactory(
        action="CHARGED", offense=dismissed_offense, severity="INFRACTION"
    )
    traffic_record = OffenseRecordFactory(
        action="CHARGED", offense=dismissed_offense, severity="TRAFFIC"
    )
    assert infraction_record not in batch.dismissed_offense_records()
    assert traffic_record in batch.dismissed_offense_records()


@pytest.mark.parametrize(
    "jurisdiction", [constants.DISTRICT_COURT, constants.SUPERIOR_COURT]
)
def test_offense_records_by_jurisdiction(batch, jurisdiction):
    """Offense records helper function should allow filtering by jurisdiction."""
    ciprs_record = CIPRSRecordFactory(jurisdiction=jurisdiction, batch=batch)
    offense = OffenseFactory(
        disposition_method=constants.DISMISSED_DISPOSITION_METHODS[0],
        ciprs_record=ciprs_record,
    )
    offense_record = OffenseRecordFactory(action="CHARGED", offense=offense)
    records = batch.dismissed_offense_records(jurisdiction=jurisdiction)
    assert offense_record in records


def test_petition_offenses(batch, record1, charged_dismissed_record):
    """Petitions should return their own offense records."""
    petition = PetitionFactory(
        form_type=constants.DISMISSED,
        jurisdiction=record1.jurisdiction,
        county=record1.county,
        batch=batch,
    )
    assert charged_dismissed_record in petition.get_all_offense_records()


def test_guilty_to_lesser(batch, record1):
    offense = OffenseFactory(
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
        plea="GUILTY TO LESSER",
        disposition_method="DISPOSED BY JUDGE",
    )

    offense_record_charged = OffenseRecordFactory(action="CHARGED", offense=offense)
    offense_record_convicted = OffenseRecordFactory(action="CONVICTED", offense=offense)

    petition = PetitionFactory(
        form_type=constants.DISMISSED,
        jurisdiction=record1.jurisdiction,
        county=record1.county,
        batch=batch,
    )

    petition_offense_records = petition.get_all_offense_records()

    assert offense_record_charged in petition_offense_records
    assert offense_record_convicted not in petition_offense_records
