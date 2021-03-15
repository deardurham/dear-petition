import datetime as dt

import pytest

from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
)
from dear_petition.petition.types import dismissed
from dear_petition.petition import constants
from dear_petition.petition.export.forms import AOCFormCR287

pytestmark = pytest.mark.django_db


@pytest.fixture
def aug1():
    return dt.date(2010, 8, 1)


@pytest.fixture
def nov1():
    return dt.date(2006, 11, 1)


@pytest.fixture
def petition(batch):
    return PetitionFactory(
        batch=batch, county="DURHAM", jurisdiction=constants.DISTRICT_COURT
    )


@pytest.fixture
def all_offenses(petition):
    return petition.get_all_offense_records()


@pytest.fixture
def cr1(batch, petition):
    return CIPRSRecordFactory(
        batch=batch,
        label=batch.label,
        jurisdiction=petition.jurisdiction,
        county=petition.county,
    )


@pytest.fixture
def cr2(batch, petition):
    return CIPRSRecordFactory(
        batch=batch, jurisdiction=petition.jurisdiction, county=petition.county,
    )


@pytest.fixture
def cr1_dismissed(cr1, aug1):
    return OffenseRecordFactory(
        action="CHARGED",
        description="MISDEMEANOR LARCENY",
        severity="MISDEMEANOR",
        offense=OffenseFactory(
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
            disposed_on=aug1,
            ciprs_record=cr1,
            jurisdiction=cr1.jurisdiction,
        ),
    )


@pytest.fixture
def cr1_guilty(cr1, aug1):
    return OffenseRecordFactory(
        action="CONVICTED",
        description="BREAK OR ENTER A MOTOR VEHICLE",
        severity="FELONY",
        offense=OffenseFactory(
            verdict="GUILTY",
            disposition_method="DISPOSED BY JUDGE",
            disposed_on=aug1,
            ciprs_record=cr1,
            jurisdiction=cr1.jurisdiction,
        ),
    )


def test_only_dismissed(all_offenses, cr1_dismissed):
    assert not dismissed.same_day_convictions(all_offenses)


def test_only_convictions(all_offenses, cr1_guilty):
    assert not dismissed.same_day_convictions(all_offenses)


def test_same_day_conviction(all_offenses, cr1_dismissed, cr1_guilty):
    assert cr1_guilty in dismissed.same_day_convictions(all_offenses)


def test_different_day_conviction(all_offenses, cr1_dismissed, cr1_guilty, cr1, nov1):
    OffenseRecordFactory(
        action="CONVICTED",
        offense__verdict="GUILTY",
        offense__disposed_on=nov1,
        offense__ciprs_record=cr1,
        offense__jurisdiction=cr1.jurisdiction,
    )
    assert [cr1_guilty] == dismissed.same_day_convictions(all_offenses)


def test_different_record(all_offenses, cr1_dismissed, cr1_guilty, cr2, aug1):
    OffenseRecordFactory(
        action="CONVICTED",
        offense__verdict="GUILTY",
        offense__disposed_on=aug1,
        offense__ciprs_record=cr2,
        offense__jurisdiction=cr2.jurisdiction,
    )
    assert [cr1_guilty] == dismissed.same_day_convictions(all_offenses)


def test_multi_same_day_convictions__same_record(
    all_offenses, cr1_dismissed, cr1_guilty, cr1, aug1
):
    other_guilty = OffenseRecordFactory(
        action="CONVICTED",
        offense__verdict="GUILTY",
        offense__disposed_on=aug1,
        offense__ciprs_record=cr1,
        offense__jurisdiction=cr1.jurisdiction,
    )
    assert [cr1_guilty, other_guilty] == dismissed.same_day_convictions(all_offenses)


def test_multi_same_day_convictions__two_records(
    all_offenses, cr1_dismissed, cr1_guilty, cr2, aug1
):
    OffenseRecordFactory(
        action="CHARGED",
        offense__disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
        offense__disposed_on=aug1,
        offense__ciprs_record=cr2,
        offense__jurisdiction=cr2.jurisdiction,
    )
    other_guilty = OffenseRecordFactory(
        action="CONVICTED",
        offense__verdict="GUILTY",
        offense__disposed_on=aug1,
        offense__ciprs_record=cr2,
        offense__jurisdiction=cr2.jurisdiction,
    )
    assert {cr1_guilty, other_guilty} == set(
        dismissed.same_day_convictions(all_offenses)
    )


def test_cr287_same_day_convictions(petition, cr1_dismissed, cr1_guilty):
    form = AOCFormCR287(petition)
    form.map_same_day_offenses()
    expected = (
        f"{cr1_guilty.offense.ciprs_record.file_no} {cr1_guilty.description.title()}"
    )
    assert form.data["ChargedDesc"] == expected
