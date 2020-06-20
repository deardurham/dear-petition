import io
import os

import pdfrw
from django.conf import settings


__all__ = ("write_pdf",)


def write_pdf(data):
    output = io.BytesIO()
    template_path = os.path.join(
        settings.APPS_DIR, "static", "templates", "AOC-CR-287.pdf"
    )
    petition = Writer(data, template_path, output)
    petition.get_annotations()
    petition.write()
    output.seek(0)
    return output


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

    def get_annotations(self):
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
