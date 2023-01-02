import os

from pdfrw import PdfDict, PdfName, PdfObject, PdfReader, PdfWriter
from django.conf import settings


__all__ = ("write_pdf",)


def write_template_and_annotations_to_stream(bytes_stream, data, form_type):
    template_path = os.path.join(
        settings.APPS_DIR, "static", "templates", f"{form_type}.pdf"
    )
    petition = Writer(data, template_path, bytes_stream)
    petition.set_annotations()
    petition.write()

def merge_acroforms(acroforms, output_form_fields):
    if not acroforms:
        return None

    output_acroform = acroforms[0]
    for source_acroform in acroforms[1:]:
        for key in source_acroform.keys():
            if key not in output_acroform:
                output_acroform[key] = source_acroform[key]

    output_acroform[PdfName('Fields')] = output_form_fields
    return output_acroform

def concatenate_pdf_streams(paths, output):
    writer = PdfWriter()
    acroforms = []
    output_form_fields = []
    for file_num, path in enumerate(paths):
        path.seek(0)
        data_bytes = path.read()
        if len(data_bytes) == 0:
            continue
        reader = PdfReader(fdata=data_bytes)
        writer.addpages(reader.pages)

        if PdfName('AcroForm') not in reader[PdfName('Root')].keys():
            continue

        # Extract PDF Acroform data and avoid form_field collisions
        # Note: This is needed to keep acroform data after merging
        # https://stackoverflow.com/a/57687160
        acroform = reader[PdfName('Root')][PdfName('AcroForm')]
        form_fields = acroform[PdfName('Fields')] if PdfName('Fields') in acroform else []
        for field_num, form_field in enumerate(form_fields):
            key = PdfName('T')
            old_name = form_field[key].replace('(','').replace(')','')  # Field names are in the "(name)" format
            form_field[key] = f'FILE_{file_num}_FIELD_{field_num}_{old_name}'

        acroforms.append(acroform)
        output_form_fields.extend(form_fields)

    output_acroform = merge_acroforms(acroforms, output_form_fields)
    if output_acroform is not None:
        writer.trailer[PdfName('Root')][PdfName('AcroForm')] = output_acroform

    writer.write(output)
    output.seek(0)


class Writer:

    ANNOT_KEY = "/Annots"
    ANNOT_FIELD_KEY = "/T"
    ANNOT_VAL_KEY = "/V"
    ANNOT_RECT_KEY = "/Rect"
    SUBTYPE_KEY = "/Subtype"
    WIDGET_SUBTYPE_KEY = "/Widget"

    def __init__(self, data, template_path, output_path):
        def read_template(template_path):
            return PdfReader(template_path)

        self.data = data
        self.output_path = output_path
        self.template = read_template(template_path)
        self.template.Root.AcroForm.update(
            PdfDict(NeedAppearances=PdfObject("true"))
        )
        self.annotations = []

    def set_annotations(self):
        self.annotations = self.template.pages[0][self.ANNOT_KEY]

    def write(self):
        for annotation in self.annotations:
            if (
                annotation[self.SUBTYPE_KEY] == self.WIDGET_SUBTYPE_KEY
                and annotation[self.ANNOT_FIELD_KEY]
            ):
                key = annotation[self.ANNOT_FIELD_KEY][1:-1]
                if key in self.data:
                    annotation.update(PdfDict(**self.data[key]))
        PdfWriter().write(self.output_path, self.template)
