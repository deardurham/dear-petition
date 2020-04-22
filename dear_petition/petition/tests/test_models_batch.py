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
    ciprs_record_1 = CIPRSRecordFactory(batch=batch, file_no="CP-100")
    ciprs_record_2 = CIPRSRecordFactory(batch=batch, file_no="CP-200")
    offense_1 = OffenseFactory(ciprs_record=ciprs_record_1)
    offense_2 = OffenseFactory(ciprs_record=ciprs_record_2)
    # OffenseRecordFactory defaults to "Action: Charged"
    offense_record_1 = OffenseRecordFactory(
        offense=offense_1, description="Offense Record 1"
    )
    offense_record_2 = OffenseRecordFactory(
        offense=offense_1, description="Offense Record 2"
    )
    offense_record_3 = OffenseRecordFactory(
        offense=offense_2, description="Offense Record 3"
    )
    offense_record_4 = OffenseRecordFactory(
        offense=offense_2, description="Offense Record 4"
    )

    petition_offenses = batch.get_petition_offenses()
    expected_file_no = [
        offense_record_1.offense.ciprs_record.file_no,
        offense_record_2.offense.ciprs_record.file_no,
        offense_record_3.offense.ciprs_record.file_no,
        offense_record_4.offense.ciprs_record.file_no,
    ]
    actual_file_no = []
    for item in petition_offenses.items():
        if "Fileno" in item[0]:
            actual_file_no.extend(item[1])
    assert len(expected_file_no) == len(actual_file_no)

    # setting the action of the offense_record_4 arraigned
    # should remove the offense_record from petition_offenses
    # dictionary
    # we'll check this by asserting that offense_record_4's
    # description is not found in the dictionary
    offense_record_4.action = ARRAIGNED
    offense_record_4.save()

    petition_offenses = batch.get_petition_offenses()
    expected_file_no = [
        offense_record_1.offense.ciprs_record.file_no,
        offense_record_2.offense.ciprs_record.file_no,
        offense_record_3.offense.ciprs_record.file_no,
    ]
    expected_descriptions = [
        offense_record_1.description,
        offense_record_2.description,
        offense_record_3.description,
    ]
    actual_file_no = []
    actual_descriptions = []
    for item in petition_offenses.items():
        if "Fileno" in item[0]:
            actual_file_no.extend(item[1])
        if "Description" in item[0]:
            actual_descriptions.extend(item[1])
    assert len(expected_file_no) == len(actual_file_no)
    description_4 = offense_record_4.description
    assert description_4 not in actual_descriptions
