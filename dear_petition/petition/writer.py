import pdfrw

from dear_petition.petition.data_dict import map_data


class Writer:

    ANNOT_KEY = "/Annots"
    ANNOT_FIELD_KEY = "/T"
    ANNOT_VAL_KEY = "/V"
    ANNOT_RECT_KEY = "/Rect"
    SUBTYPE_KEY = "/Subtype"
    WIDGET_SUBTYPE_KEY = "/Widget"

    def __init__(self, form_data, batch, template_path, output_path):
        def read_template(template_path):
            return pdfrw.PdfReader(template_path)

        self.data = map_data(form_data, batch)
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
