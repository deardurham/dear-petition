import pytest
from django.utils import timezone

from dear_petition.petition import constants
from dear_petition.petition import models as pm
from dear_petition.petition.tests.factories import (
    BatchFactory,
    BatchFileFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
    CIPRSRecordFactory,
    ClientFactory,
)
from dear_petition.petition.etl.load import link_offense_records, create_documents
from dear_petition.petition.etl.transform import recalculate_petitions, combine_batches

pytestmark = pytest.mark.django_db


def test_recalculate_petitions(petition):
    batch = petition.batch
    record = CIPRSRecordFactory(batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM")
    offense = OffenseFactory(
        disposition_method="Dismissed by Court",
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

    assert petition.offense_records.filter(petitionoffenserecord__active=True).count() == 12
    assert petition.has_attachments()
    recalculate_petitions(petition.id, offense_record_ids)
    assert petition.offense_records.filter(petitionoffenserecord__active=True).count() == 5
    assert not petition.has_attachments()


def test_combine_batches(batch, batch_file, fake_pdf):
    record = CIPRSRecordFactory(batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM")
    record.refresh_record_from_data()

    second_batch = BatchFactory()

    second_record_data = {
        "General": {"County": "DURHAM", "File No": "00GR000001"},
        "Case Information": {
            "Case Status": "DISPOSED",
            "Offense Date": "2018-01-01T20:00:00",
        },
        "Defendant": {
            "Date of Birth/Estimated Age": "1990-01-01",
            "Name": "DOE,JON,BOJACK",
            "Race": "WHITE",
            "Sex": "M",
        },
        "District Court Offense Information": [
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "SPEEDING(80 mph in a 65 mph zone)",
                        "Severity": "TRAFFIC",
                        "Law": "20-141(J1)",
                        "Code": "4450",
                    },
                ],
                "Disposed On": "2018-02-01",
                "Disposition Method": "DISPOSED BY JUDGE",
            },
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "SPEEDING(80 mph in a 65 mph zone)",
                        "Severity": "TRAFFIC",
                        "Law": "20-141(J1)",
                        "Code": "4450",
                    },
                ],
                "Disposed On": "2018-02-01",
                "Disposition Method": "DISPOSED BY JUDGE",
            },
        ],
        "Superior Court Offense Information": [],
    }
    second_batch_file = BatchFileFactory(batch=second_batch, file=fake_pdf)

    second_record = CIPRSRecordFactory(
        batch=second_batch,
        data=second_record_data,
        batch_file=second_batch_file,
        jurisdiction=constants.DISTRICT_COURT,
        county="DURHAM",
    )
    second_record.refresh_record_from_data()

    assert batch.records.count() == 1
    assert pm.Offense.objects.filter(ciprs_record__batch__id=batch.id).count() == 1
    assert pm.Offense.objects.filter(ciprs_record__batch__id=second_batch.id).count() == 2
    assert batch.files.count() == 1

    new_label = "Combined Batch"
    user_id = batch.user_id
    new_batch = combine_batches([batch.id, second_batch.id], label=new_label, user_id=user_id)

    assert new_batch.records.count() == 2
    assert pm.Offense.objects.filter(ciprs_record__batch__id=new_batch.id).count() == 3
    assert (
        pm.OffenseRecord.objects.filter(offense__ciprs_record__batch__id=new_batch.id).count() == 4
    )
    assert new_batch.files.count() == 2
    assert new_batch.label == new_label
    assert new_batch.user_id == user_id
