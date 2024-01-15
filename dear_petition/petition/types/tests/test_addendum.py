from unittest import mock

import pytest

from dear_petition.petition.types import addendum
from dear_petition.petition import models as pm

pytestmark = pytest.mark.django_db


def test_calculate_checkmark_3b_string(offense_record1, offense_record2):
    checkmark_3b_string = addendum.calculate_checkmark_3b_string([offense_record1, offense_record2])
    assert (
        checkmark_3b_string
        == f"{offense_record1.file_no} {offense_record1.description}, {offense_record2.file_no} {offense_record2.description}"
    )


def test_create_checkmark_3b_addendum_form_with_no_records(petition, petition_document):
    addendum.create_checkmark_3b_addendum_form(petition, petition_document)
    assert not petition.base_document.form_specific_data["is_checkmark_3b_checked"]


@mock.patch(
    "dear_petition.petition.types.addendum.calculate_checkmark_3b_string",
    return_value="Record 1",
)
def test_create_checkmark_3b_addendum_form_with_records(
    mock_function,
    petition,
    petition_document,
    charged_dismissed_record,
    convicted_guilty_record,
):
    petition.offense_records.add(charged_dismissed_record)
    petition.offense_records.add(convicted_guilty_record)
    pm.PetitionOffenseRecord.objects.filter(
        petition=petition, offense_record=convicted_guilty_record
    ).update(active=False)
    addendum.create_checkmark_3b_addendum_form(petition, petition_document)
    assert petition.base_document.form_specific_data["is_checkmark_3b_checked"]
    assert petition.base_document.form_specific_data["charged_desc_string"] is not None


@mock.patch(
    "dear_petition.petition.types.addendum.calculate_checkmark_3b_string",
    return_value="Record 1, Record 2, Record 3, Record 4, Record 5, Record 6, Record 7, Record 8, Record 9, Record 10, Record 11, Record 12, Record 13, Record 14, Record 15, Record 16, Record 17, Record 18, Record 19, Record 20",
)
def test_create_checkmark_3b_addendum_form_with_too_many_records(
    mock_function,
    petition,
    petition_document,
    charged_dismissed_record,
    convicted_guilty_record,
):
    petition.offense_records.add(charged_dismissed_record)
    petition.offense_records.add(convicted_guilty_record)
    pm.PetitionOffenseRecord.objects.filter(
        petition=petition, offense_record=convicted_guilty_record
    ).update(active=False)
    addendum.create_checkmark_3b_addendum_form(petition, petition_document)
    assert petition.base_document.form_specific_data["is_checkmark_3b_checked"]
    assert petition.base_document.form_specific_data["charged_desc_string"] == "See addendum"
