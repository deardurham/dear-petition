from .annotate import add_pdf_template_annotations
from .mapper import build_pdf_template_context
from .writer import write_pdf


__all__ = ("generate_petition_pdf",)


def generate_petition_pdf(petition, extra):
    context = build_pdf_template_context(petition, extra)
    add_pdf_template_annotations(context)
    generate_petition_pdf = write_pdf(context, form_type=petition.form_type)
    return generate_petition_pdf
