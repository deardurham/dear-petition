import pytest
from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
)
from dear_petition.petition.constants import CHARGED, ARRAIGNED

pytestmark = pytest.mark.django_db


def test_batch_most_recent_record_none(batch, record1):
    del record1.data["Case Information"]["Offense Date"]
    record1.save()
    assert batch.most_recent_record
