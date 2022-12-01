import io
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

def concatenate_pdf_streams(paths, output):
    writer = PdfWriter()
    output_acroform = None
    for file_num, path in enumerate(paths):
        path.seek(0)
        bytes = path.read()
        if len(bytes) == 0:
            continue
        reader = PdfReader(fdata=bytes)
        writer.addpages(reader.pages)

        # Not all PDFs have an AcroForm node
        if PdfName('AcroForm') not in reader[PdfName('Root')].keys():
            continue

        source_acroform = reader[PdfName('Root')][PdfName('AcroForm')]
        output_formfields = source_acroform[PdfName('Fields')] if PdfName('Fields') in source_acroform else []
        for field_num, form_field in enumerate(output_formfields):
            key = PdfName('T')
            old_name = form_field[key].replace('(','').replace(')','')  # Field names are in the "(name)" format
            form_field[key] = f'FILE_{file_num}_FIELD_{field_num}_{old_name}'

        if output_acroform == None:
            # copy the first AcroForm node
            output_acroform = source_acroform
        else:
            for key in source_acroform.keys():
                # Add new AcroForms keys if output_acroform already existing
                if key not in output_acroform:
                    output_acroform[key] = source_acroform[key]

            # Add missing font entries in /DR node of source file
            if (PdfName('DR') in source_acroform.keys()) and (PdfName('Font') in source_acroform[PdfName('DR')].keys()):
                if PdfName('Font') not in output_acroform[PdfName('DR')].keys():
                    # if output_acroform is missing entirely the /Font node under an existing /DR, simply add it
                    output_acroform[PdfName('DR')][PdfName('Font')] = source_acroform[PdfName('DR')][PdfName('Font')]
                else:
                    # else add new fonts only
                    for font_key in source_acroform[PdfName('DR')][PdfName('Font')].keys():
                        if font_key not in output_acroform[PdfName('DR')][PdfName('Font')]:
                            output_acroform[PdfName('DR')][PdfName('Font')][font_key] = source_acroform[PdfName('DR')][PdfName('Font')][font_key]

        if PdfName('Fields') not in output_acroform:
            output_acroform[PdfName('Fields')] = output_formfields
        else:
            # Add new fields
            output_acroform[PdfName('Fields')] += output_formfields

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
