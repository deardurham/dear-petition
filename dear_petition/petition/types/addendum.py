from dear_petition.petition import constants as pc
from dear_petition.petition import models as pm
from dear_petition.petition import utils as pu
from . import addendum_3b


def create_addendum_documents(petition, previous_document):
    if petition.form_type in ADDENDUM_FORMS_TYPE_MAP:
        addendum_document_creator = ADDENDUM_FORMS_TYPE_MAP[petition.form_type]
        addendum_document_creator(petition, previous_document)


def calculate_checkmark_3b_string(offense_records):
    offense_record_strings = [
        f"{offense_record.file_no} {offense_record.description}"
        for offense_record in offense_records
    ]
    checkmark_3b_string = ", ".join(offense_record_strings)
    return checkmark_3b_string


def create_checkmark_3b_addendum_form(petition, previous_document):
    ADDENDUM_3B_FIRST_LINE_LIMIT = 242
    ADDENDUM_3B_SECOND_LINE_LIMIT = 410
    ADDENDUM_3B_PIXEL_LIMIT = (
        ADDENDUM_3B_FIRST_LINE_LIMIT + ADDENDUM_3B_SECOND_LINE_LIMIT
    )
    qs = addendum_3b.get_offense_records(petition)
    if not qs.exists():
        petition.base_document.form_specific_data["is_checkmark_3b_checked"] = False
    else:
        checkmark_3b_string = calculate_checkmark_3b_string(qs)
        checkmark_3b_string_pixel_length = pu.get_text_pixel_length(checkmark_3b_string)
        if checkmark_3b_string_pixel_length > ADDENDUM_3B_PIXEL_LIMIT:
            addendum_3b_document = pm.PetitionDocument.objects.create(
                petition=petition,
                previous_document=previous_document,
                form_type=pc.ADDENDUM_3B,
            )
            addendum_3b_document.offense_records.add(*qs)
            petition.base_document.form_specific_data["is_checkmark_3b_checked"] = True
            petition.base_document.form_specific_data[
                "charged_desc_string"
            ] = "See addendum"
        else:
            petition.base_document.form_specific_data["is_checkmark_3b_checked"] = True
            truncation_point = pu.get_truncation_point_of_text_by_pixel_size(
                checkmark_3b_string, ADDENDUM_3B_FIRST_LINE_LIMIT
            )
            petition.base_document.form_specific_data[
                "charged_desc_string"
            ] = checkmark_3b_string[0:truncation_point]
            petition.base_document.form_specific_data[
                "charged_desc_cont_string"
            ] = checkmark_3b_string[truncation_point:]

    petition.base_document.save()


ADDENDUM_FORMS_TYPE_MAP = {pc.DISMISSED: create_checkmark_3b_addendum_form}
