import pytest
from .factories import (
    BatchFactory,
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
)
from ..constants import CHARGED, ARRAIGNED

pytestmark = pytest.mark.django_db


def test_batch_most_recent_record_none(batch, record1):
    del record1.data["Case Information"]["Offense Date"]
    record1.save()
    assert batch.most_recent_record


def test_get_petition_offenses():
    batch = BatchFactory()
    ciprs_record_1 = CIPRSRecordFactory(batch=batch)
    ciprs_record_2 = CIPRSRecordFactory(batch=batch)
    offense_1 = OffenseFactory(ciprs_record=ciprs_record_1)
    offense_2 = OffenseFactory(ciprs_record=ciprs_record_2)
    # OffenseRecordFactory defaults to "Action: Charged"
    offense_record_1 = OffenseRecordFactory(offense=offense_1)
    offense_record_2 = OffenseRecordFactory(offense=offense_1)
    offense_record_3 = OffenseRecordFactory(offense=offense_2)
    offense_record_4 = OffenseRecordFactory(offense=offense_2)

    petition_offenses = batch.get_petition_offenses()
    assert petition_offenses.get(f"Fileno:{4}").get("V") == ciprs_record_2.file_no
    assert (
        petition_offenses.get(f"Description:{4}").get("V")
        == offense_record_4.description
    )
    assert petition_offenses.get(f"Fileno:{5}") is None
    assert petition_offenses.get(f"Description:{5}") is None

    offense_record_4.action = ARRAIGNED
    offense_record_4.save()
    # Now only 3 offense records have the action of "CHARGED"
    petition_offenses = batch.get_petition_offenses()
    assert petition_offenses.get(f"Fileno:{3}").get("V") == ciprs_record_2.file_no
    assert (
        petition_offenses.get(f"Description:{3}").get("V")
        == offense_record_4.description
    )
    assert petition_offenses.get(f"Fileno:{4}") is None
    assert petition_offenses.get(f"Description:{4}") is None
