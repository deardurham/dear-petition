import pytest

from dear_petition.petition.tests.factories import CIPRSRecordFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def data():
    return {
        "District Court Offense Information": [
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "PWISD MARIJUANA",
                        "Severity": "FELONY",
                        "Law": "G.S. 90-95(A)",
                    }
                ],
                "Disposed On": "2001-01-01",
                "Disposition Method": "DISMISSAL WITHOUT LEAVE BY DA",
            },
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "POSSESS DRUG PARAPHERNALIA",
                        "Severity": "MISDEMEANOR",
                        "Law": "G.S. 90-113.22(A)",
                    }
                ],
                "Disposed On": "2001-02-01",
                "Disposition Method": "DISMISSED BY COURT",
            },
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "RESISTING PUBLIC OFFICER",
                        "Severity": "MISDEMEANOR",
                        "Law": "G.S. 14-223",
                    },
                    {
                        "Action": "CONVICTED",
                        "Description": "RESISTING PUBLIC OFFICER",
                        "Severity": "MISDEMEANOR",
                        "Law": "G.S. 14-223",
                    },
                ],
                "Disposed On": "2001-03-01",
                "Disposition Method": "DISPOSED BY JUDGE",
            },
        ],
        "Superior Court Offense Information": [],
    }


@pytest.fixture
def record(data):
    rec = CIPRSRecordFactory(data=data)
    rec.refresh_record_from_data()
    rec.refresh_from_db()
    return rec


def test_offense__disposed_on(record1):
    val = "2001-01-01"
    record1.data = {"District Court Offense Information": [{"Disposed On": val}]}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    offense = record1.offenses.first()
    assert offense.disposed_on.strftime("%Y-%m-%d") == val


def test_offense__disposition_method(record1):
    val = "DISMISSAL WITHOUT LEAVE BY DA"
    record1.data = {"District Court Offense Information": [{"Disposition Method": val}]}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    offense = record1.offenses.first()
    assert offense.disposition_method == val


def test_offense_record(record):
    offense = record.offenses.get(disposed_on="2001-01-01")
    offense_record = offense.offense_records.first()
    assert offense_record.action == "CHARGED"
    assert offense_record.description == "PWISD MARIJUANA"
    assert offense_record.severity == "FELONY"
    assert offense_record.law == "G.S. 90-95(A)"


def test_offense_record__multi(record):
    offense = record.offenses.get(disposed_on="2001-03-01")
    assert offense.offense_records.count() == 2
