from docxtpl import DocxTemplate
from django.conf import settings

from dear_petition.petition import helpers
from dear_petition.petition import models as pm
from dear_petition.petition.types.dismissed import (
    get_offense_records as get_dismissed_records,
)
from dear_petition.petition.types.underaged_convictions import (
    get_offense_records as get_underaged_conviction_records,
)

TEMPLATE = "advice_letter.docx"


def template_offense_records(qs):
    """
    Takes a queryset of offense records and turns them into the template format the document requires.
    """


def generate_context(batch, contact, petitioner_info):
    context = {}
    context["first_name"], context["last_name"] = helpers.split_first_and_last_name(
        batch.label
    )
    context["address"] = petitioner_info["address1"]
    context["address_second_line"] = petitioner_info["address2"]
    context["city"] = petitioner_info["city"]
    context["state"] = petitioner_info["state"]
    context["zipcode"] = petitioner_info["zipCode"]
    context["felonies"] = [
        felony
        for felony in pm.OffenseRecord.objects.filter(
            offense__ciprs_record__batch=batch, severity="FELONY"
        )
    ]
    context["misdemeanors"] = [
        misdemeanor
        for misdemeanor in pm.OffenseRecord.objects.filter(
            offense__ciprs_record__batch=batch, severity="MISDEMEANOR"
        )
    ]
    context["underaged"] = [
        conviction for conviction in get_underaged_conviction_records(batch)
    ]
    context["dismissed"] = [conviction for conviction in get_dismissed_records(batch)]
    context["phone_number"] = contact.phone_number
    context["email"] = contact.email
    context["attorney_name"] = contact.name

    return context


def generate_advice_letter(batch, contact, petitioner_info):

    context = generate_context(batch, contact, petitioner_info)
    doc = DocxTemplate(settings.TEMPLATE_DIR.path(TEMPLATE))
    doc.render(context)

    return doc
