import random
from pytz import timezone

import factory

from dear_petition.petition.models import (
    CIPRSRecord,
    Batch,
    Offense,
    OffenseRecord,
    Petition,
    PetitionOffenseRecord,
    PetitionDocument,
    Contact,
    GeneratedPetition,
)
from dear_petition.users.tests.factories import UserFactory

from ..constants import (
    CHARGED,
    CONVICTED,
    DISMISSED,
    DISTRICT_COURT,
    SUPERIOR_COURT,
    DURHAM_COUNTY,
    DISTRICT_COURT_WITHOUT_DA_LEAVE,
    FEMALE,
    MALE,
    NOT_AVAILABLE,
    UNKNOWN,
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
                    "Severity": "TRAFFIC",
                    "Law": "20-141(J1)",
                    "Code": "4450",
                },
                {
                    "Action": "ARRAIGNED",
                    "Description": "SPEEDING(80 mph in a 65 mph zone)",
                    "Severity": "INFRACTION",
                    "Law": "G.S. 20-141(B)",
                    "Code": "4450",
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
    offense_date = factory.Faker("date_time", tzinfo=timezone("US/Eastern"))
    arrest_date = factory.Faker("date_object")
    jurisdiction = factory.LazyFunction(
        lambda: random.choice([DISTRICT_COURT, SUPERIOR_COURT])
    )
    county = factory.LazyFunction(lambda: random.choice(["DURHAM", "WAKE", "ORANGE"]))
    file_no = "99CRAAAAAAAAAAAA"
    race = factory.LazyFunction(lambda: random.choice(["ASIAN", "BLACK", "WHITE"]))
    sex = factory.LazyFunction(
        lambda: random.choice([FEMALE, MALE, NOT_AVAILABLE, UNKNOWN])
    )

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
    law = "20-141(J1)"
    code = "4450"
    action = CHARGED
    severity = "TRAFFIC"
    description = "SPEEDING(96 mph in a 70 mph zone) "

    class Meta:
        model = OffenseRecord


class PetitionFactory(factory.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    county = DURHAM_COUNTY
    form_type = DISMISSED
    jurisdiction = DISTRICT_COURT

    class Meta:
        model = Petition


class PetitionOffenseRecordFactory(factory.DjangoModelFactory):
    petition = factory.SubFactory(PetitionFactory)
    offense_record = factory.SubFactory(OffenseRecordFactory)
    active = True

    class Meta:
        model = PetitionOffenseRecord


class DismissedOffenseRecordFactory(factory.DjangoModelFactory):
    offense = factory.SubFactory(
        OffenseFactory, disposition_method=DISTRICT_COURT_WITHOUT_DA_LEAVE
    )
    law = "20-141(J1)"
    code = "4450"
    action = CHARGED
    severity = "TRAFFIC"
    description = "SPEEDING(96 mph in a 70 mph zone) "

    class Meta:
        model = OffenseRecord


class GuiltyOffenseRecordFactory(factory.DjangoModelFactory):
    offense = factory.SubFactory(
        OffenseFactory, disposition_method=DISTRICT_COURT_WITHOUT_DA_LEAVE
    )
    law = "20-141(J1)"
    code = "4450"
    action = "Guilty"
    severity = "TRAFFIC"
    description = "SPEEDING(96 mph in a 70 mph zone) "

    class Meta:
        model = OffenseRecord


class PetitionDocumentFactory(factory.DjangoModelFactory):
    petition = factory.SubFactory(PetitionFactory)
    form_type = DISMISSED

    class Meta:
        model = PetitionDocument


class ContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contact

class ClientFactory(factory.DjangoModelFactory):
    category = 'client'

    class Meta:
        model = Contact


class AttorneyFactory(factory.DjangoModelFactory):
    category = 'attorney'

    class Meta:
        model = Contact


class GeneratedPetitionFactory(factory.DjangoModelFactory):
    form_type = DISMISSED
    number_of_charges = 1
    batch_id = 1

    class Meta:
        model = GeneratedPetition
