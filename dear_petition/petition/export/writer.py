import io
import os

import pdfrw
from django.conf import settings


__all__ = ("write_pdf",)


def write_template_and_annotations_to_stream(bytes_stream, data, form_type):
    template_path = os.path.join(
        settings.APPS_DIR, "static", "templates", f"{form_type}.pdf"
    )
    petition = Writer(data, template_path, bytes_stream)
    petition.set_annotations()
    petition.write()

def concatenate_pdf_streams(paths, output):
    writer = pdfrw.PdfWriter()

    for path in paths:
        path.seek(0)
        bytes = path.read()
        if len(bytes) == 0:
            continue
        reader = pdfrw.PdfReader(fdata=bytes)
        writer.addpages(reader.pages)

    writer.write(output)


class Writer:

    ANNOT_KEY = "/Annots"
    ANNOT_FIELD_KEY = "/T"
    ANNOT_VAL_KEY = "/V"
    ANNOT_RECT_KEY = "/Rect"
    SUBTYPE_KEY = "/Subtype"
    WIDGET_SUBTYPE_KEY = "/Widget"

    def __init__(self, data, template_path, output_path):
        def read_template(template_path):
            return pdfrw.PdfReader(template_path)

        self.data = data
        self.output_path = output_path
        self.template = read_template(template_path)
        self.template.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true"))
        )

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
                    annotation.update(pdfrw.PdfDict(**self.data[key]))
        pdfrw.PdfWriter().write(self.output_path, self.template)
