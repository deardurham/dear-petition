import pytest

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)
from dear_petition.petition.constants import CONVICTED, CHARGED
from dear_petition.petition.models import Offense, OffenseRecord

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "action, disposition_method, should_be_included",
    [
        # records that have data as they would from Portal (no action)
        ("", "No Probable Cause Found", True),
        (
            "",
            "District Guilty - Judge",
            False,
        ),  # exclude because not Portal dismissed disposition method
        # records that have data as they would from CIPRS (disposition_method not one seen in Portal)
        (CHARGED, "No Probable Cause", True),
        (CONVICTED, "No Probable Cause", False),  # exclude because not charged action
        (
            CHARGED,
            "Disposed By Judge",
            False,
        ),  # exclude because not CIPRS dismissed disposition method
    ],
)
def test_dismissed(action, disposition_method, should_be_included, batch, record1):
    offense = Offense.objects.create(
        ciprs_record=record1,
        disposition_method=disposition_method,
    )
    offense_record = OffenseRecord.objects.create(
        offense=offense,
        action=action,
    )

    if should_be_included:
        assert offense_record in batch.dismissed_offense_records()
    else:
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


@pytest.mark.parametrize("jurisdiction", [constants.DISTRICT_COURT, constants.SUPERIOR_COURT])
def test_offense_records_by_jurisdiction(batch, jurisdiction):
    """Offense records helper function should allow filtering by jurisdiction."""
    ciprs_record = CIPRSRecordFactory(jurisdiction=jurisdiction, batch=batch)
    offense = OffenseFactory(
        disposition_method=constants.CIPRS_DISPOSITION_METHODS_DISMISSED[0],
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
