from .mapper import build_pdf_template_context
from .writer import write_pdf


__all__ = ("generate_petition_pdf",)


def generate_petition_pdf(petition, extra):
    context = build_pdf_template_context(petition, extra)
    buffer = write_pdf(context)
    return buffer
