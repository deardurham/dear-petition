import tempfile

from django import forms

from dear_petition.petition.models import CIPRSRecord


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
