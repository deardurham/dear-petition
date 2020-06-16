import pytest

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
