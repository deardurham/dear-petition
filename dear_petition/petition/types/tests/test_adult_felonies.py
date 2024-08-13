import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import OffenseRecord

pytestmark = pytest.mark.django_db


def test_adult_felony_included(batch, adult_convicted_guilty_record):
    adult_convicted_guilty_record.severity = constants.SEVERITIES.FELONY
    adult_convicted_guilty_record.save()

    assert adult_convicted_guilty_record in batch.adult_felony_records()


def test_adult_misdemeanor_not_included(batch, adult_convicted_guilty_record):
    adult_convicted_guilty_record.severity = constants.SEVERITIES.MISDEMEANOR
    adult_convicted_guilty_record.save()

    assert adult_convicted_guilty_record not in batch.adult_felony_records()
