from django.conf import settings
from docxtpl import DocxTemplate

from dear_petition.petition import constants as pc

TEMPLATE = "3b_addendum.docx"


def generate_context(petition_document):
    client = petition_document.petition.batch.client

    context = {}
    context["county"] = petition_document.petition.county.upper()
    context["name"] = client.name.upper()
    context[
        "file_no"
    ] = (
        petition_document.offense_records.first().file_no.upper()
    )  # Just need one example, will be followed by 'et al' in document
    context["jurisdiction"] = (
        "SUPERIOR COURT DIVISION"
        if petition_document.petition.jurisdiction == pc.SUPERIOR_COURT
        else "DISTRICT COURT DIVISION"
    )
    context["offense_records"] = petition_document.offense_records.all()

    return context


def generate_3b_addendum(petition_document):
    context = generate_context(petition_document)
    doc = DocxTemplate(settings.TEMPLATE_DIR.path(TEMPLATE))
    doc.render(context)

    return doc
