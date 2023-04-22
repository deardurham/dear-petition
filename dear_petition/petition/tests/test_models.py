from datetime import datetime

import pytest
import pytz
from django.db import IntegrityError

from dear_petition.petition.constants import (
    DISMISSED,
    DISTRICT_COURT,
    DURHAM_COUNTY,
    DISP_METHOD_SUPERSEDING_INDICTMENT,
    DISP_METHOD_WAIVER_OF_PROBABLE_CAUSE,
    VERDICT_GUILTY,
    VERDICT_GUILTY_TO_LESSER,
    VERDICT_RESPONSIBLE,
    VERDICT_RESPONSIBLE_TO_LESSER,
    CHARGED,
    CONVICTED,
    FEMALE,
    MALE
)
from dear_petition.petition.models import GeneratedPetition
from dear_petition.petition.tests.factories import OffenseFactory, OffenseRecordFactory
from dear_petition.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_printable_model_mixin__petition(batch, petition, contact1, contact2, offense_record1):
    """
    Test PrintableModelMixin repr() method using Petition model because Petition has many to many
    relationships.
    """

    # set many to many relationships
    petition.agencies.add(contact1)
    petition.agencies.add(contact2)
    petition.offense_records.add(offense_record1)

    # assertions
    expected_repr = ", ".join([
        "{'id': " + repr(petition.id),
        "'created': " + repr(petition.created),
        "'modified': " + repr(petition.modified),
        "'form_type': 'AOC-CR-287'",
        "'batch': " + repr(batch.id),
        "'county': 'DURHAM'",
        "'jurisdiction': 'D'",
        "'offense_records': [" + repr(offense_record1.id) + "]",
        "'agencies': [" + repr(contact1.id) + ", " + repr(contact2.id) + "]}"
    ])
    assert(repr(petition) == expected_repr)


def test_printable_model_mixin__user():
    """
    Test PrintableModelMixin repr() method using User model because User has a field that should be excluded.
    """

    # create model object
    user = UserFactory(username="tmarshall", email="tmarshall@supremecourt.gov", name="Thurgood Marshall")

    # assertions
    expected_repr = ", ".join([
        "{'id': " + repr(user.id),
        "'last_login': None",
        "'is_superuser': False",
        "'username': 'tmarshall'",
        "'first_name': ''",
        "'last_name': ''",
        "'email': 'tmarshall@supremecourt.gov'",
        "'is_staff': False",
        "'is_active': True",
        "'date_joined': " + repr(user.date_joined),
        "'name': 'Thurgood Marshall'",
        "'last_generated_petition_time': None",
        "'groups': []",
        "'user_permissions': []}"
    ])
    assert(repr(user) == expected_repr)


@pytest.mark.parametrize("input_dob, input_today, expected_age", [
    # has had birthday already this year
    (datetime(2000, 1, 1), datetime(2030, 7, 15, 0, 0, 0, 0, pytz.UTC), 30),
    # has not had birthday yet this year
    (datetime(2000, 12, 31), datetime(2030, 7, 15, 0, 0, 0, 0, pytz.UTC), 29),
    # tomorrow is birthday
    (datetime(2000, 7, 15), datetime(2020, 7, 14, 23, 59, 59, 999999, pytz.UTC), 19),
    # today is birthday
    (datetime(2000, 7, 15), datetime(2020, 7, 15, 0, 0, 0, 0, pytz.UTC), 20),
    # born today
    (datetime(2020, 7, 15), datetime(2020, 7, 15, 0, 0, 0, 0, pytz.UTC), 0),
    # born 100+ years ago
    (datetime(1920, 7, 15), datetime(2020, 7, 15, 0, 0, 0, 0, pytz.UTC), 100),
    # age < 0 (dob mistake)
    (datetime(2070, 1, 1), datetime(2020, 7, 15, 0, 0, 0, 0, pytz.UTC), -50),
])
def test_batch__age(mocker, batch, record0, input_dob, input_today, expected_age):
    """
    Test age in Batch
    """

    # mock today's date
    now_date_mock = mocker.patch("django.utils.timezone.now")
    now_date_mock.return_value = input_today

    # create 3 CIPRS records and only the middle one has value for date of birth
    record0(None, "ASIAN", FEMALE)
    record0(input_dob, "ASIAN", FEMALE)
    record0(None, "ASIAN", FEMALE)

    # assertions
    assert(batch.age == expected_age)


def test_batch__age_no_dob(batch, record0):
    """
    Test age in Batch when there is no dob on any CIPRS record
    """

    # create CIPRS record with no date of birth
    record0(None, "ASIAN", FEMALE)

    # assertions
    assert(batch.age is None)


def test_batch__race(batch, record0):
    """
    Test race in Batch
    """

    # test constants
    RACE = "WHITE"

    # create CIPRS record
    record0(None, RACE, FEMALE)

    # assertions
    assert(batch.race == RACE)


def test_batch__sex(batch, record0):
    """
    Test sex in Batch
    """

    # test constants
    SEX = MALE

    # create CIPRS record
    record0(None, "BLACK", SEX)

    # assertions
    assert(batch.sex == SEX)


def test_generated_petition__get_stats_generated_petition(mocker, charged_dismissed_record, charged_not_guilty_record,
    petition_document, user):
    """
    Test get_stats_generated_petition in GeneratedPetition
    """

    # test constants
    TODAY = datetime(2022, 12, 10, 0, 0, 0, 0, pytz.UTC)
    AGE = 42
    RACE = "ASIAN"
    SEX = FEMALE
    USERNAME = "user1"
    OFFENSE_RECORDS = [charged_dismissed_record, charged_not_guilty_record]

    # mock today's date
    now_date_mock = mocker.patch("django.utils.timezone.now")
    now_date_mock.return_value = TODAY

    # set username and offense records
    user.username = USERNAME
    petition_document.offense_records.set(OFFENSE_RECORDS)

    # get stats for generated petition
    generated_petition = GeneratedPetition.get_stats_generated_petition(petition_document.id, user)

    # assertions
    assert(generated_petition.username == USERNAME)
    assert(generated_petition.form_type == DISMISSED)
    assert(generated_petition.number_of_charges == len(OFFENSE_RECORDS))
    assert(generated_petition.batch_id == petition_document.petition.batch.id)
    assert(generated_petition.age == AGE)
    assert(generated_petition.race == RACE)
    assert(generated_petition.sex == SEX)
    assert(generated_petition.jurisdiction == DISTRICT_COURT)
    assert(generated_petition.county == DURHAM_COUNTY)
    assert(user.last_generated_petition_time == TODAY)


def test_generated_petition__get_stats_generated_petition__dob_after_today(mocker, petition_document, record0, user):
    """
    Test get_stats_generated_petition in GeneratedPetition when date of birth on CIPRS record (mistakenly) is after
    today
    """

    # test constants
    TODAY = datetime(2022, 12, 10, 0, 0, 0, 0, pytz.UTC)
    DOB = datetime(2072, 1, 1)

    # mock today's date
    now_date_mock = mocker.patch("django.utils.timezone.now")
    now_date_mock.return_value = TODAY

    # create mistake CIPRS record with date of birth after today
    record0(DOB, "WHITE", MALE)

    # test should pass if error raised
    with pytest.raises(IntegrityError):

        # get stats for generated petition
        generated_petition = GeneratedPetition.get_stats_generated_petition(petition_document.id, user)


def test_offense__is_convicted_of_charged():
    """
    Test is_convicted_of_charged in Offense. Should return true.
    """
    offense = OffenseFactory(verdict = VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(offense.is_convicted_of_charged())


def test_offense__is_convicted_of_charged__different_descriptions():
    """
    Test is_convicted_of_charged in Offense. Should return false because descriptions are different.
    """
    offense = OffenseFactory(verdict = VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="COMMUNICATING THREATS", severity="MISDEMEANOR")

    assert(not offense.is_convicted_of_charged())


def test_offense__is_convicted_of_charged__different_severities():
    """
    Test is_convicted_of_charged in Offense. Should return false because severities are different.
    """
    offense = OffenseFactory(verdict = VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="FELONY")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(not offense.is_convicted_of_charged())


def test_offense__is_convicted_of_charged__not_guilty():
    """
    Test is_convicted_of_charged in Offense. Should return false because verdict is not GUILTY.
    """
    offense = OffenseFactory(verdict = "NOT GUILTY")
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(not offense.is_convicted_of_charged())


def test_offense__is_guilty_to_lesser__different_descriptions():
    """
    Test is_guilty_to_lesser in Offense. Should return true because descriptions are different.
    """
    offense = OffenseFactory(verdict=VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="COMMUNICATING THREATS", severity="MISDEMEANOR")

    assert(offense.is_guilty_to_lesser())


def test_offense__is_guilty_to_lesser__different_severities():
    """
    Test is_guilty_to_lesser in Offense. Should return true because severities are different.
    """
    offense = OffenseFactory(verdict=VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="FELONY")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(offense.is_guilty_to_lesser())


def test_offense__is_guilty_to_lesser__equivalent_offenses():
    """
    Test is_guilty_to_lesser in Offense. Should return false because offenses are equivalent.
    """
    offense = OffenseFactory(verdict=VERDICT_GUILTY)
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(not offense.is_guilty_to_lesser())


def test_offense__is_guilty_to_lesser__not_guilty():
    """
    Test is_guilty_to_lesser in Offense. Should return false because verdict is not GUILTY.
    """
    offense = OffenseFactory(verdict="NOT GUILTY")
    OffenseRecordFactory(offense=offense, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(not offense.is_guilty_to_lesser())


def test_offense__has_equivalent_offense_records__equivalent(offense1):
    """
    Test has_equivalent_offense_records in Offense. Should return true.
    """
    OffenseRecordFactory(offense=offense1, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense1, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(offense1.has_equivalent_offense_records())


def test_offense__has_equivalent_offense_records__different_descriptions(offense1):
    """
    Test has_equivalent_offense_records in Offense. Should return false because descriptions are different.
    """
    OffenseRecordFactory(offense=offense1, action=CHARGED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")
    OffenseRecordFactory(offense=offense1, action=CONVICTED, description="COMMUNICATING THREATS", severity="MISDEMEANOR")

    assert(not offense1.has_equivalent_offense_records())


def test_offense__has_equivalent_offense_records__different_severities(offense1):
    """
    Test has_equivalent_offense_records in Offense. Should return false because severities are different.
    """
    OffenseRecordFactory(offense=offense1, action=CHARGED, description="SIMPLE ASSAULT", severity="FELONY")
    OffenseRecordFactory(offense=offense1, action=CONVICTED, description="SIMPLE ASSAULT", severity="MISDEMEANOR")

    assert(not offense1.has_equivalent_offense_records())


def test_offense__has_equivalent_offense_records__one_offense_record(offense1):
    """
    Test has_equivalent_offense_records in Offense. Should return false because there is only one offense record.
    """
    OffenseRecordFactory(offense=offense1, action=CHARGED, description="SIMPLE ASSAULT", severity="FELONY")

    assert(not offense1.has_equivalent_offense_records())


@pytest.mark.parametrize("verdict", [VERDICT_GUILTY, VERDICT_RESPONSIBLE])
def test_offense__is_visible__equivalent(verdict):
    """
    Test is_visible in Offense when the verdict is GUILTY or RESPONSIBLE and the offense records are equivalent.
    The CHARGED offense record should not be visible and the CONVICTED offense record should be visible.
    """
    offense = OffenseFactory(verdict=verdict)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert not offense_record_charged.is_visible
    assert offense_record_convicted.is_visible


@pytest.mark.parametrize("verdict", [VERDICT_GUILTY, VERDICT_RESPONSIBLE])
def test_offense__is_visible__not_equivalent_description(verdict):
    """
    Test is_visible in Offense when the verdict is GUILTY or RESPONSIBLE and the offense records have
    descriptions that are not equivalent. The CHARGED and CONVICTED offense records should be visible.
    """
    offense = OffenseFactory(verdict=verdict)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="COMMUNICATING THREATS",
        severity="MISDEMEANOR"
    )

    assert offense_record_charged.is_visible
    assert offense_record_convicted.is_visible


@pytest.mark.parametrize("verdict", [VERDICT_GUILTY, VERDICT_RESPONSIBLE])
def test_offense__is_visible__not_equivalent_severity(verdict):
    """
    Test is_visible in Offense when the verdict is GUILTY or RESPONSIBLE and the offense records have serverities
    that are not equivalent. The CHARGED and CONVICTED offense records should be visible.
    """
    offense = OffenseFactory(verdict=verdict)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="FELONY"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert offense_record_charged.is_visible
    assert offense_record_convicted.is_visible


@pytest.mark.parametrize("verdict", [VERDICT_GUILTY, VERDICT_RESPONSIBLE])
def test_offense__is_visible__one_offense_record(verdict):
    """
    Test is_visible in Offense when the verdict is GUILTY or RESPONSIBLE and there is only one offense record. It
    should be visible.
    """
    offense = OffenseFactory(verdict=verdict)
    offense_record = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert offense_record.is_visible


def test_offense__is_visible__not_convicted():
    """
    Test is_visible in Offense when the verdict is not GUILTY or RESPONSIBLE. The CHARGED and CONVICTED offense
    records should be visible.
    """
    offense = OffenseFactory(verdict="JUDGMENT ARRESTED")
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert offense_record_charged.is_visible
    assert offense_record_convicted.is_visible


@pytest.mark.parametrize("disp_method", [DISP_METHOD_SUPERSEDING_INDICTMENT, DISP_METHOD_WAIVER_OF_PROBABLE_CAUSE])
def test_offense__is_visible__excluded_disp_method(disp_method):
    """
    Test is_visible in Offense when the disposition method is excluded. No offense records should be visible.
    """
    offense = OffenseFactory(verdict=VERDICT_GUILTY, disposition_method=disp_method)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert not offense_record_charged.is_visible
    assert not offense_record_convicted.is_visible

def test_offense__disposition__no_verdict():
    """
    Test disposition in Offense when there is no verdict. The offense record's disposition should be the
    offense's disposition method.
    """
    offense = OffenseFactory(disposition_method="NO PROBABLE CAUSE", verdict="")
    offense_record = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert offense_record.disposition == "NO PROBABLE CAUSE"


def test_offense__disposition__verdict():
    """
    Test disposition in Offense when there is a verdict. The offense record's disposition should be the offense's
    verdict.
    """
    offense = OffenseFactory(disposition_method="NO PROBABLE CAUSE", verdict="JUDGMENT ARRESTED")
    offense_record = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )

    assert offense_record.disposition == "JUDGMENT ARRESTED"


def test_offense__disposition__guilty_to_lesser():
    """
    Test disposition in Offense when offense is "guilty to lesser". The CHARGED offense record's disposition
    should be GUILTY TO LESSER. The CONVICTED offense record's disposition should be GUILTY.
    """
    offense = OffenseFactory(disposition_method="DISPOSED BY JUDGE", verdict=VERDICT_GUILTY)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="COMMUNICATING THREATS",
        severity="MISDEMEANOR"
    )

    assert offense_record_charged.disposition == VERDICT_GUILTY_TO_LESSER
    assert offense_record_convicted.disposition == VERDICT_GUILTY


def test_offense__disposition__responsible_to_lesser():
    """
    Test disposition in Offense when offense is "responsible to lesser". The CHARGED offense record's disposition
    should be RESPONSIBLE TO LESSER. The CONVICTED offense record's disposition should be RESPONSIBLE.
    """
    offense = OffenseFactory(disposition_method="DISPOSED BY JUDGE", verdict=VERDICT_RESPONSIBLE)
    offense_record_charged = OffenseRecordFactory(
        offense=offense,
        action=CHARGED,
        description="SIMPLE ASSAULT",
        severity="MISDEMEANOR"
    )
    offense_record_convicted = OffenseRecordFactory(
        offense=offense,
        action=CONVICTED,
        description="COMMUNICATING THREATS",
        severity="MISDEMEANOR"
    )

    assert offense_record_charged.disposition == VERDICT_RESPONSIBLE_TO_LESSER
    assert offense_record_convicted.disposition == VERDICT_RESPONSIBLE
