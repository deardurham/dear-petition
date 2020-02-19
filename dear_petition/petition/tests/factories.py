from typing import Any, Sequence

from django.contrib.auth import get_user_model
import factory


from dear_petition.petition.models import CIPRSRecord, Batch
from dear_petition.users.tests.factories import UserFactory


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

    class Meta:
        model = CIPRSRecord
