import io
from .annotate import add_pdf_template_annotations
from .forms import (
    AOCFormCR287,
    AOCFormCR285,
    AOCFormCR288,
    AOCFormCR293,
    DataPetitionForm,
)
from .writer import concatenate_pdf_streams, write_template_and_annotations_to_stream

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
    assert form_type in FORM_TYPE_MAP, 'Invalid form type provided'
    Form = FORM_TYPE_MAP.get(form_type)
    form = Form(petition_document, extra=extra)
    form.build_form_context()
    return form.data


def generate_petition_pdf(petition_documents, extra):
    pdf_stream = io.BytesIO()
    doc_streams = []
    for petition_document in petition_documents:
        doc_stream = io.BytesIO()
        context = build_pdf_template_context(petition_document, extra)
        add_pdf_template_annotations(context)
        write_template_and_annotations_to_stream(doc_stream, context, petition_document.form_type)
        doc_streams.append(doc_stream)
    concatenate_pdf_streams(doc_streams, pdf_stream)
    for doc_stream in doc_streams:
        doc_stream.close()
    return pdf_stream
