from .annotate import add_pdf_template_annotations
from .forms import (
    AOCFormCR287,
    AOCFormCR285,
    AOCFormCR288,
    AOCFormCR293,
    DataPetitionForm,
)
from .writer import write_pdf

from dear_petition.petition import constants


__all__ = ("generate_petition_pdf",)


FORM_TYPE_MAP = {
    constants.DATA_PETITION: DataPetitionForm,
    constants.DISMISSED: AOCFormCR287,
    constants.ATTACHMENT: AOCFormCR285,
    constants.NOT_GUILTY: AOCFormCR288,
    constants.UNDERAGED_CONVICTIONS: AOCFormCR293,
}


def build_pdf_template_context(petition_document, extra):
    if hasattr(petition_document, "data_only") and petition_document.data_only:
        form_type = constants.DATA_PETITION
    else:
        form_type = petition_document.form_type
    Form = FORM_TYPE_MAP.get(form_type, AOCFormCR287)
    form = Form(petition_document, extra=extra)
    form.build_form_context()
    return form.data


def generate_petition_pdf(petition_document, extra):
    context = build_pdf_template_context(petition_document, extra)
    add_pdf_template_annotations(context)
    generate_petition_pdf = write_pdf(context, form_type=petition_document.form_type)
    return generate_petition_pdf
