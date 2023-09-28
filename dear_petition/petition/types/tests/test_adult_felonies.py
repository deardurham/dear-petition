import pytest

from dear_petition.petition import constants
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)

pytestmark = pytest.mark.django_db


def test_adult_felony_included(batch, record1, convicted_guilty_record):
    convicted_guilty_record.severity = constants.SEVERITIES.FELONY
    convicted_guilty_record.save()

    assert convicted_guilty_record in batch.adult_felony_records()


def test_adult_misdemeanor_not_included(batch, record1, convicted_guilty_record):
    convicted_guilty_record.severity = constants.SEVERITIES.MISDEMEANOR
    convicted_guilty_record.save()

    assert convicted_guilty_record not in batch.adult_felony_records()
