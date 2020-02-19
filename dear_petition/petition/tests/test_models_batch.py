import pytest

pytestmark = pytest.mark.django_db


def test_batch_most_recent_record_none(batch, record1):
    del record1.data["Case Information"]["Offense Date"]
    record1.save()
    assert batch.most_recent_record
