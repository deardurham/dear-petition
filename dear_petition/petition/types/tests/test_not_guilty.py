import pytest

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    OffenseRecordFactory,
    PetitionFactory,
    CIPRSRecordFactory,
    OffenseFactory,
)
from dear_petition.petition.constants import (
    CONVICTED,
    CHARGED,
    SEVERITIES,
    VERDICT_GUILTY,
    VERDICT_NOT_GUILTY,
)
from dear_petition.petition.models import Offense, OffenseRecord

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "action, verdict, disposition_method, should_be_included",
    [
        # records that have data as they would from Portal (no action or verdict)
        ("", "", "District Not Guilty - Judge", True),
        (
            "",
            "",
            "District Guilty - Judge",
            False,
        ),  # exclude because not Portal not-guilty disposition method
        # records that have data as they would from CIPRS (disposition_method not one seen in Portal)
        (CHARGED, VERDICT_NOT_GUILTY, "Disposed By Judge", True),
        (
            CONVICTED,
            VERDICT_NOT_GUILTY,
            "Disposed By Judge",
            False,
        ),  # exclude because not charged action
        (
            CHARGED,
            VERDICT_GUILTY,
            "Disposed By Judge",
            False,
        ),  # exclude because not not-guilty verdict
        (
            CHARGED,
            VERDICT_NOT_GUILTY,
            "Dismissed by Court",
            False,
        ),  # exclude because meets dismissed criteria
    ],
)
def test_not_guilty(action, verdict, disposition_method, should_be_included, batch, record1):
    offense = Offense.objects.create(
        ciprs_record=record1,
        verdict=verdict,
        disposition_method=disposition_method,
    )
    offense_record = OffenseRecord.objects.create(
        offense=offense,
        action=action,
    )

    if should_be_included:
        assert offense_record in batch.not_guilty_offense_records()
    else:
        assert offense_record not in batch.not_guilty_offense_records()


@pytest.mark.parametrize("file_no_type,should_be_included", [["CR", True], ["IF", False]])
def test_infraction_severity_offense_record(batch, file_no_type, should_be_included):
    """Offense records with severity INFRACTION in the file number should be excluded if "IF" is in file no and included if "CR" is in file no."""
    record = CIPRSRecordFactory(batch=batch, file_no=f"99{file_no_type}BBBBBBBBBBBB")
    not_guilty_offense = OffenseFactory(
        ciprs_record=record, jurisdiction=constants.DISTRICT_COURT, verdict="Not Guilty"
    )
    infraction_record = OffenseRecordFactory(
        action="CHARGED", offense=not_guilty_offense, severity="INFRACTION"
    )
    traffic_record = OffenseRecordFactory(
        action="CHARGED", offense=not_guilty_offense, severity="TRAFFIC"
    )

    infraction_is_included = infraction_record in batch.not_guilty_offense_records()
    assert infraction_is_included is should_be_included
    assert traffic_record in batch.not_guilty_offense_records()


def test_non_not_guilty_infraction_not_included(batch, record1):
    offense = Offense.objects.create(
        ciprs_record=record1,
        verdict=VERDICT_GUILTY,
        disposition_method="Not a valid disposition method.",
    )
    offense_record = OffenseRecord.objects.create(
        offense=offense, action=CONVICTED, severity=SEVERITIES.INFRACTION
    )

    assert offense_record not in batch.not_guilty_offense_records()


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
