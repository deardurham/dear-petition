import io
import random

import factory
from dear_petition.petition.models import (Batch, BatchFile, CIPRSRecord,
                                           Contact, Agency, Client, GeneratedPetition, Offense,
                                           OffenseRecord, Petition,
                                           PetitionDocument,
                                           PetitionOffenseRecord)
from dear_petition.users.tests.factories import UserFactory
from django.core.files.uploadedfile import InMemoryUploadedFile
from pytz import timezone

from ..constants import (CHARGED, CONVICTED, DISMISSED, DISTRICT_COURT,
                         DISTRICT_COURT_WITHOUT_DA_LEAVE, DURHAM_COUNTY,
                         FEMALE, MALE, NOT_AVAILABLE, SUPERIOR_COURT, UNKNOWN)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact


class AgencyFactory(factory.django.DjangoModelFactory):
    category = "agency"

    class Meta:
        model = Agency


class ClientFactory(factory.django.DjangoModelFactory):
    category = "client"

    class Meta:
        model = Client


class AttorneyFactory(factory.django.DjangoModelFactory):
    category = "attorney"

    class Meta:
        model = Contact


class BatchFactory(factory.django.DjangoModelFactory):
    label = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Batch


def fake_file(filename, content_type):
    output = io.StringIO("blahblah")
    stream = io.BytesIO(output.getvalue().encode("utf-8"))
    file_ = InMemoryUploadedFile(
        file=stream,
        field_name=None,
        name=filename,
        content_type=content_type,
        size=stream.getbuffer().nbytes,
        charset=None,
    )
    return file_


class BatchFileFactory(factory.django.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    date_uploaded = factory.Faker("date_time", tzinfo=timezone("US/Eastern"))
    file = fake_file("fakefile.pdf", "pdf")

    class Meta:
        model = BatchFile


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
            }
        ],
        "Superior Court Offense Information": [],
    }


class CIPRSRecordFactory(factory.django.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    batch_file = factory.SubFactory(BatchFileFactory)
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


class OffenseFactory(factory.django.DjangoModelFactory):
    ciprs_record = factory.SubFactory(CIPRSRecordFactory)
    disposed_on = factory.Faker("date_object")
    disposition_method = "DISPOSED BY JUDGE"

    class Meta:
        model = Offense


class OffenseRecordFactory(factory.django.DjangoModelFactory):
    offense = factory.SubFactory(OffenseFactory)
    law = "20-141(J1)"
    code = "4450"
    action = CHARGED
    severity = "TRAFFIC"
    description = "SPEEDING(96 mph in a 70 mph zone) "

    class Meta:
        model = OffenseRecord


class PetitionFactory(factory.django.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    county = DURHAM_COUNTY
    form_type = DISMISSED
    jurisdiction = DISTRICT_COURT

    class Meta:
        model = Petition


class PetitionOffenseRecordFactory(factory.django.DjangoModelFactory):
    petition = factory.SubFactory(PetitionFactory)
    offense_record = factory.SubFactory(OffenseRecordFactory)
    active = True

    class Meta:
        model = PetitionOffenseRecord


class DismissedOffenseRecordFactory(factory.django.DjangoModelFactory):
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


class GuiltyOffenseRecordFactory(factory.django.DjangoModelFactory):
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


class PetitionDocumentFactory(factory.django.DjangoModelFactory):
    petition = factory.SubFactory(PetitionFactory)
    form_type = DISMISSED

    class Meta:
        model = PetitionDocument


class GeneratedPetitionFactory(factory.django.DjangoModelFactory):
    form_type = DISMISSED
    number_of_charges = 1
    batch_id = 1

    class Meta:
        model = GeneratedPetition
