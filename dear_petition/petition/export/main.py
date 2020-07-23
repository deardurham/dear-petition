from .annotate import add_pdf_template_annotations
from .forms import AOCFormCR287, AOCFormCR285
from .writer import write_pdf

from dear_petition.petition import constants


__all__ = ("generate_petition_pdf",)


FORM_TYPE_MAP = {
    constants.DISMISSED: AOCFormCR287,
    constants.ATTACHMENT: AOCFormCR285,
}


def build_pdf_template_context(petition, extra):
    Form = FORM_TYPE_MAP.get(petition.form_type, AOCFormCR287)
    form = Form(petition, extra=extra)
    form.build_form_context()
    return form.data


def generate_petition_pdf(petition, extra):
    context = build_pdf_template_context(petition, extra)
    add_pdf_template_annotations(context)
    generate_petition_pdf = write_pdf(context, form_type=petition.form_type)
    return generate_petition_pdf
