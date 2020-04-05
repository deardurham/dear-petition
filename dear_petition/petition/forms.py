import io
import os

from django import forms
from django.conf import settings

from dear_petition.petition.models import CIPRSRecord, Contact, Batch
from dear_petition.petition.writer import Writer
from dear_petition.petition.data_dict import map_data


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    def save(self, user):
        batch = Batch.objects.create(user=user)
        records = []
        for idx, file_ in enumerate(self.files.getlist("files")):
            record = CIPRSRecord(batch=batch)
            if settings.CIPRS_SAVE_PDF:
                record.report_pdf = file_
            record.data = record.parse_report(file_)
            if "error" in record.data:
                raise forms.ValidationError(record.data["error"])
            if "Defendant" in record.data and "Name" in record.data["Defendant"]:
                label = record.data["Defendant"]["Name"]
                if idx == 0:
                    batch.label = label   
                elif label != batch.label:
                    raise forms.ValidationError(f"We were provided one record with the name {batch.label} and another with the name {label}. All records must have the same name.")         
                record.label = label
            records.append(record)

        batch.save()
        CIPRSRecord.objects.bulk_create(records)
        batch.records.add(*records)

        return batch


class GeneratePetitionForm(forms.Form):

    attorney = forms.ModelChoiceField(
        queryset=Contact.objects.filter(category="attorney"), required=False
    )
    agency1 = forms.ModelChoiceField(
        queryset=Contact.objects.filter(category="agency"),
        label="Agency #1",
        required=False,
    )
    agency2 = forms.ModelChoiceField(
        queryset=Contact.objects.filter(category="agency"),
        label="Agency #2",
        required=False,
    )
    as_attachment = forms.BooleanField(
        required=False, help_text="Download PDF as an attachment (off by default)"
    )

    def __init__(self, *args, **kwargs):
        self.batch = kwargs.pop("batch")
        super().__init__(*args, **kwargs)

    def clean_attorney(self):
        data = self.cleaned_data["attorney"]
        if data:
            return {
                "NameAtty": data.name,
                "StAddrAtty": data.address1,
                "MailAddrAtty": data.address2,
                "CityAtty": data.city,
                "StateAtty": data.state,
                "ZipCodeAtty": data.zipcode,
            }

    def clean_agency1(self):
        data = self.cleaned_data["agency1"]
        if data:
            return {
                "NameAgency1": data.name,
                "AddrAgency1": data.address1,
                "MailAgency1": data.address2,
                "CityAgency1": data.city,
                "StateAgency1": data.state,
                "ZipAgency1": data.zipcode,
            }

    def clean_agency2(self):
        data = self.cleaned_data["agency2"]
        if data:
            return {
                "NameAgency2": data.name,
                "AddrAgency2": data.address1,
                "MailAgency2": data.address2,
                "CityAgency2": data.city,
                "StateAgency2": data.state,
                "ZipAgency2": data.zipcode,
            }

    def clean(self):
        cleaned_data = super().clean()
        if not self.batch.most_recent_record:
            raise forms.ValidationError(
                "All associated CIPRS records are missing offense dates"
            )
        # Run map_data() now so we can raise exceptions as form errors
        try:
            map_data(cleaned_data, self.batch)
        except Exception as e:
            raise forms.ValidationError(str(e))

    def save(self):
        output = io.BytesIO()
        template_path = os.path.join(
            settings.APPS_DIR, "static", "templates", "petition-template.pdf"
        )
        form_data = self.cleaned_data.copy()
        del form_data["as_attachment"]
        petition = Writer(form_data, self.batch, template_path, output)
        petition.get_annotations()
        petition.write()
        output.seek(0)
        return output
