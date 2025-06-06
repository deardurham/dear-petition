import string
from datetime import datetime
from datetime import date

from django.utils import timezone
import pytest

from dear_petition.petition.constants import CHARGED, CONVICTED, FEMALE
from dear_petition.petition.tests.factories import (
    BatchFactory,
    BatchFileFactory,
    CIPRSRecordFactory,
    ClientFactory,
    PetitionFactory,
    PetitionOffenseRecordFactory,
    PetitionDocumentFactory,
    ContactFactory,
    OffenseFactory,
    OffenseRecordFactory,
    fake_file,
)
from dear_petition.petition.types import dismissed
from dear_petition.petition import constants
from dear_petition.petition.etl.paginator import OffenseRecordPaginator


@pytest.fixture
def data():
    return {}


@pytest.fixture
def extra():
    return {}


@pytest.fixture
def batch(user):
    yield BatchFactory(user=user)


@pytest.fixture
def record0(batch):
    def _record0(dob: datetime, race: string, sex: string):
        """
        For example, create a CIPRS Record with:
        record0(datetime(1994, 12, 31), "ASIAN", "F")
        """
        CIPRSRecordFactory(batch=batch, label=batch.label, dob=dob, race=race, sex=sex)

    yield _record0


@pytest.fixture
def record1(batch):
    yield CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=constants.DISTRICT_COURT,
        dob=datetime(1980, 7, 7),
        race="ASIAN",
        sex=FEMALE,
    )


@pytest.fixture
def record2(batch):
    yield CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=constants.DISTRICT_COURT,
        county=constants.DURHAM_COUNTY,
    )


@pytest.fixture
def offense1(record2):
    yield OffenseFactory(
        ciprs_record=record2,
        disposition_method=constants.DISTRICT_COURT_WITHOUT_DA_LEAVE,
    )


@pytest.fixture
def offense_record1(offense1, petition, petition_document):
    record = OffenseRecordFactory(offense=offense1)
    PetitionOffenseRecordFactory(petition=petition, offense_record=record)
    record.documents.set([petition_document])
    yield record


@pytest.fixture
def offense_record2(offense1, petition, petition_document):
    record = OffenseRecordFactory(offense=offense1)
    PetitionOffenseRecordFactory(petition=petition, offense_record=record)
    record.documents.set([petition_document])
    yield record


@pytest.fixture
def fake_pdf():
    return fake_file("sample.pdf", "pdf")


@pytest.fixture
def fake_pdf2():
    return fake_file("sample2.pdf", "pdf")


@pytest.fixture
def batch_file(batch):
    return BatchFileFactory(batch=batch)


@pytest.fixture
def petition(batch):
    return PetitionFactory(batch=batch)


@pytest.fixture
def petition_document(petition):
    return PetitionDocumentFactory(petition=petition)


@pytest.fixture
def contact1():
    return ContactFactory(
        name="George",
        address1="111 Test Lane",
        address2="Apt E",
        city="Durham",
        state="NC",
        zipcode="27701",
    )


@pytest.fixture
def contact2():
    return ContactFactory(
        name="Colin",
        address1="222 Also Test Ln",
        address2="",
        city="Durham",
        state="NC",
        zipcode="27702",
    )


@pytest.fixture
def contact3():
    return ContactFactory(
        name="Chris",
        address1="333 Still A Test Parkway",
        address2="#404",
        city="Durham",
        state="NC",
        zipcode="27703",
    )


@pytest.fixture
def client():
    return ClientFactory(
        name="Test Name",
        address1="123 Test Ct",
        address2="Apt A",
        city="Durham",
        state="NC",
        zipcode="27701",
        dob=timezone.now().date(),  # I wasn't born yesterday
    )


@pytest.fixture
def dismissed_offense(record1):
    return OffenseFactory(
        disposition_method=dismissed.CIPRS_DISPOSITION_METHODS_DISMISSED[0],
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
    )


@pytest.fixture
def non_dismissed_offense(record1):
    return OffenseFactory(disposition_method="OTHER", ciprs_record=record1)


@pytest.fixture
def charged_dismissed_record(dismissed_offense):
    return OffenseRecordFactory(action=CHARGED, offense=dismissed_offense)


@pytest.fixture
def charged_not_guilty_record(not_guilty_offense):
    return OffenseRecordFactory(action=CHARGED, offense=not_guilty_offense)


@pytest.fixture
def guilty_offense(record1):
    return OffenseFactory(
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
        verdict="GUILTY",
        disposition_method="",
    )


@pytest.fixture
def convicted_guilty_record(guilty_offense):
    yield OffenseRecordFactory(action=CONVICTED, offense=guilty_offense)


@pytest.fixture
def not_guilty_offense(record1):
    return OffenseFactory(
        ciprs_record=record1,
        jurisdiction=constants.DISTRICT_COURT,
        verdict="Not Guilty",
    )


@pytest.fixture
def paginator(petition):
    return OffenseRecordPaginator(petition)
