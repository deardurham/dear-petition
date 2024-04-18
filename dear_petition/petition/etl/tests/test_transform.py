import pytest

from dear_petition.petition import constants
from dear_petition.petition import models as pm
from dear_petition.petition.tests.factories import (
    BatchFactory,
    BatchFileFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
    CIPRSRecordFactory,
)
from dear_petition.petition.etl.load import link_offense_records, create_documents
from dear_petition.petition.etl.transform import recalculate_petitions, combine_batches

pytestmark = pytest.mark.django_db


def test_recalculate_petitions(petition):
    petition = PetitionFactory(form_type=constants.UNDERAGED_CONVICTIONS)
    batch = petition.batch
    record = CIPRSRecordFactory(
        batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM"
    )
    offense = OffenseFactory(
        disposition_method="PROBATION OTHER",
        ciprs_record=record,
        jurisdiction=constants.DISTRICT_COURT,
    )
    offense_record_ids = []
    for i in range(12):
        offense_record = OffenseRecordFactory(offense=offense, action="CHARGED")
        petition.offense_records.add(offense_record)
        if len(offense_record_ids) < 5:
            offense_record_ids.append(offense_record.id)
    link_offense_records(petition)
    create_documents(petition)

    assert (
        petition.offense_records.filter(petitionoffenserecord__active=True).count()
        == 12
    )
    assert petition.has_attachments()
    recalculate_petitions(petition.id, offense_record_ids)
    assert (
        petition.offense_records.filter(petitionoffenserecord__active=True).count() == 5
    )
    assert not petition.has_attachments()


def test_combine_batches(batch, batch_file, fake_pdf):
    batch_label = batch.label
    record = CIPRSRecordFactory(
        batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM"
    )
    offense = OffenseFactory(
        disposition_method="PROBATION OTHER",
        ciprs_record=record,
        jurisdiction=constants.DISTRICT_COURT,
    )
    offense_record = OffenseRecordFactory(offense=offense, action="CHARGED")

    second_batch = BatchFactory()
    second_batch_file = BatchFileFactory(batch=second_batch, file=fake_pdf)
    second_batch_label = second_batch.label
    second_record = CIPRSRecordFactory(
        batch=second_batch, batch_file=second_batch_file, jurisdiction=constants.DISTRICT_COURT, county="DURHAM"
    )
    second_offense = OffenseFactory(
        disposition_method="PROBATION OTHER",
        ciprs_record=second_record,
        jurisdiction=constants.DISTRICT_COURT,
    )
    second_offense_record = OffenseRecordFactory(offense=second_offense, action="CHARGED")
    third_offense = OffenseFactory(
        disposition_method="PROBATION OTHER",
        ciprs_record=second_record,
        jurisdiction=constants.SUPERIOR_COURT,
    )
    third_offense_record = OffenseRecordFactory(offense=third_offense, action="CHARGED")
  
    assert batch.records.count() == 1
    assert pm.Offense.objects.filter(ciprs_record__batch__id=batch.id).count() == 1
    assert pm.Offense.objects.filter(ciprs_record__batch__id=second_batch.id).count() == 2
    assert batch.files.count() == 1

    new_label = "Combined Batch"
    new_batch = combine_batches([batch.id, second_batch.id], label=new_label, user_id=batch.user.id)

    assert new_batch.records.count() == 2
    assert pm.Offense.objects.filter(ciprs_record__batch__id=new_batch.id).count() == 2
    assert new_batch.files.count() == 2

    