import pytest

from dear_petition.petition.utils import make_datetime_aware

pytestmark = pytest.mark.django_db


def test_general_file_no(record1):
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.file_no == record1.data["General"]["File No"]


def test_general_county(record1):
    record1.data = {"General": {"County": "DURHAM"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.county == record1.data["General"]["County"]


def test_defendant_dob(record1):
    record1.data = {"Defendant": {"Date of Birth/Estimated Age": "2000-01-01"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert (
        record1.dob.strftime("%Y-%m-%d")
        == record1.data["Defendant"]["Date of Birth/Estimated Age"]
    )


def test_defendant_sex(record1):
    record1.data = {"Defendant": {"Sex": "M"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.sex == record1.data["Defendant"]["Sex"]


def test_defendant_race(record1):
    record1.data = {"Defendant": {"Race": "WHITE"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.race == record1.data["Defendant"]["Race"]


def test_case_information_case_status(record1):
    record1.data = {"Case Information": {"Case Status": "DISPOSED"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.case_status == record1.data["Case Information"]["Case Status"]


def test_case_information_offense_date(record1):
    record1.data = {"Case Information": {"Offense Date": "2000-01-01T00:00:00"}}
    expected = make_datetime_aware(record1.data["Case Information"]["Offense Date"])
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.offense_date == expected


def test_case_information_arrest_date(record1):
    record1.data = {"Case Information": {"Arrest Date": "2000-01-01"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert (
        record1.arrest_date.strftime("%Y-%m-%d")
        == record1.data["Case Information"]["Arrest Date"]
    )
