import io
import json
import os
import tempfile

from django import forms
from django.conf import settings

from dear_petition.petition.models import CIPRSRecord
from dear_petition.petition.writer import Writer
from dear_petition.petition.data_dict import map_data
from dear_petition.petition.writer import Writer


class UploadFileForm(forms.Form):
    file = forms.FileField(label="CIRPS Detail Report")

    def save(self):
        file_ = self.cleaned_data['file']
        record = CIPRSRecord()
        record.data = record.parse_report(file_)
        if 'error' in record.data:
            raise forms.ValidationError(record.data['error'])
        if 'Defendant' in record.data and 'Name' in record.data['Defendant']:
            record.label = record.data['Defendant']['Name']
        record.save()
        return record


class GeneratePetitionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.record = kwargs.pop('record')
        super().__init__(*args, **kwargs)

    def save(self):
        output = io.BytesIO()
        template_path = os.path.join(settings.APPS_DIR, 'static', 'templates', 'petition-template.pdf')
        petition = Writer(
            self.record.data,
            map_data,
            template_path,
            output,
        )
        petition.get_annotations()
        petition.write()
        output.seek(0)
        return output
