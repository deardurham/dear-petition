import random

import factory

from dear_petition.petition.models import (
    CIPRSRecord,
    Batch,
    Offense,
    OffenseRecord,
    Petition,
    Contact,
)
from dear_petition.users.tests.factories import UserFactory

from ..constants import (
    CHARGED,
    DISMISSED,
    DISTRICT_COURT,
    SUPERIOR_COURT,
    DURHAM_COUNTY,
)


class BatchFactory(factory.DjangoModelFactory):

    label = factory.Faker("name")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Batch


def record_data(idx):
    return {
        "General": {"County": "DURHAM", "File No": "00GR000000"},
        "Case Information": {
            "Case Status": "DISPOSED",
            "Offense Date": "2018-01-01T20:00:00",
        },
        "Defendant": {
            "Date of Birth/Estimated Age": "1990-01-01",
            "Name": "DOE,JON,BOJACK",
            "Race": "WHITE",
            "Sex": "MALE",
        },
        "Offense Record": {
            "Records": [
                {
                    "Action": "CHARGED",
                    "Description": "SPEEDING(80 mph in a 65 mph zone)",
                    "Severity": "INFRACTION",
                    "Law": "G.S. 20-141(B)",
                    "Code": "4450",
                },
                {
                    "Action": "ARRAIGNED",
                    "Description": "SPEEDING(80 mph in a 65 mph zone)",
                    "Severity": "INFRACTION",
                    "Law": "G.S. 20-141(B)",
                    "Code": "4450",
                },
                {
                    "Action": "CONVICTED",
                    "Description": "IMPROPER EQUIP - SPEEDOMETER",
                    "Severity": "INFRACTION",
                    "Law": "G.S. 20-123.2",
                    "Code": "4418",
                },
            ],
            "Disposed On": "2018-02-01",
            "Disposition Method": "DISPOSED BY JUDGE",
        },
    }


class CIPRSRecordFactory(factory.DjangoModelFactory):

    batch = factory.SubFactory(BatchFactory)
    label = factory.Faker("name")
    data = factory.Sequence(record_data)
    jurisdiction = factory.LazyFunction(
        lambda: random.choice([DISTRICT_COURT, SUPERIOR_COURT])
    )
    county = factory.LazyFunction(lambda: random.choice(["DURHAM", "WAKE", "ORANGE"]))

    class Meta:
        model = CIPRSRecord


class OffenseFactory(factory.DjangoModelFactory):
    ciprs_record = factory.SubFactory(CIPRSRecordFactory)
    disposed_on = factory.Faker("date_object")
    disposition_method = "DISPOSED BY JUDGE"

    class Meta:
        model = Offense


class OffenseRecordFactory(factory.DjangoModelFactory):
    offense = factory.SubFactory(OffenseFactory)
    law = "G.S. 20-141(B)"
    code = "4450"
    action = CHARGED
    severity = "INFRACTION"
    description = "SPEEDING(80 mph in a 65 mph zone)"

    class Meta:
        model = OffenseRecord


class PetitionFactory(factory.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    county = DURHAM_COUNTY
    form_type = DISMISSED
    jurisdiction = DISTRICT_COURT

    class Meta:
        model = Petition


class ContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contact
