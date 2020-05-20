import pytest

from dear_petition.petition.types import dismissed
from dear_petition.petition.tests.factories import OffenseFactory, OffenseRecordFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def dismissed_offense(record1):
    yield OffenseFactory(
        disposition_method=dismissed.DISPOSITION_METHODS[0], ciprs_record=record1
    )


@pytest.fixture
def non_dismissed_offense(record1):
    yield OffenseFactory(disposition_method="OTHER", ciprs_record=record1)


@pytest.mark.parametrize("method", dismissed.DISPOSITION_METHODS)
def test_charged_disposition_methods(batch, record1, method):
    """CHARGED offense records should be included for all dismissed disposition methods."""
    offense = OffenseFactory(disposition_method=method, ciprs_record=record1)
    offense_record = OffenseRecordFactory(action="CHARGED", offense=offense)
    assert offense_record in batch.dismissed_offense_records()


def test_non_charged_offense_record(batch, dismissed_offense):
    """Non-CHARGED dismissed offense records should be exlucded."""
    offense_record = OffenseRecordFactory(action="CONVICTED", offense=dismissed_offense)
    assert offense_record not in batch.dismissed_offense_records()


def test_non_dismissed_disposition_method(batch, non_dismissed_offense):
    """Offenses with non-dismissed disposition methods should be exlucded."""
    offense_record = OffenseRecordFactory(
        action="CHARGED", offense=non_dismissed_offense
    )
    assert offense_record not in batch.dismissed_offense_records()
