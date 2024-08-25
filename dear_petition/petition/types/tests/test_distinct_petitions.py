import pytest

from dear_petition.petition import constants
from dear_petition.petition.types import dismissed, identify_distinct_petitions
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
)

pytestmark = pytest.mark.django_db


def test_distinct_petition(batch, dismissed_offense):
    """Expected jurisdiction and county should be in identified petition types."""
    OffenseRecordFactory(action="CHARGED", offense=dismissed_offense)
    petition_types = identify_distinct_petitions(batch.dismissed_offense_records())
    expected = {
        "jurisdiction": dismissed_offense.ciprs_record.jurisdiction,
        "county": dismissed_offense.ciprs_record.county,
    }
    assert [expected] == list(petition_types)


def test_distinct_petition__many(batch):
    """Identified petitions should include unique pairing of jurisdiction and county."""
    method = constants.CIPRS_DISPOSITION_METHODS_DISMISSED[0]
    for jurisdiction in [constants.DISTRICT_COURT, constants.SUPERIOR_COURT]:
        for county in ["DURHAM", "WAKE"]:
            record = CIPRSRecordFactory(
                jurisdiction=jurisdiction, county=county, batch=batch
            )
            offense = OffenseFactory(disposition_method=method, ciprs_record=record)
            OffenseRecordFactory(action="CHARGED", offense=offense)
    petition_types = identify_distinct_petitions(batch.dismissed_offense_records())
    assert petition_types.count() == 4
    for jurisdiction in [constants.DISTRICT_COURT, constants.SUPERIOR_COURT]:
        for county in ["DURHAM", "WAKE"]:
            assert {"jurisdiction": jurisdiction, "county": county} in petition_types


def test_distinct_petition__distinct_ciprs_records(batch):
    """A distinct list of county/jurisdiction pairs should be returned."""
    record1 = CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=constants.DISTRICT_COURT,
        county=constants.DURHAM_COUNTY,
    )
    OffenseRecordFactory(
        action="CHARGED",
        offense=OffenseFactory(
            disposition_method=dismissed.CIPRS_DISPOSITION_METHODS_DISMISSED[0],
            ciprs_record=record1,
        ),
    )
    record2 = CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=constants.DISTRICT_COURT,
        county=constants.DURHAM_COUNTY,
    )
    OffenseRecordFactory(
        action="CHARGED",
        offense=OffenseFactory(
            disposition_method=dismissed.CIPRS_DISPOSITION_METHODS_DISMISSED[0],
            ciprs_record=record2,
        ),
    )
    petition_types = identify_distinct_petitions(batch.dismissed_offense_records())
    expected = {
        "jurisdiction": record1.jurisdiction,
        "county": record1.county,
    }
    assert [expected] == list(petition_types)
