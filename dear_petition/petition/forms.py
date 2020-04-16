import io
import os

from django import forms
from django.conf import settings

from dear_petition.petition.models import (
    CIPRSRecord,
    Offense,
    OffenseRecord,
    Contact,
    Batch,
)
from dear_petition.petition.writer import Writer
from dear_petition.petition.data_dict import map_data


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    def save(self, user):
        batch = Batch.objects.create(user=user)
        for idx, file_ in enumerate(self.files.getlist("files")):
            record = CIPRSRecord(batch=batch)
            if settings.CIPRS_SAVE_PDF:
                record.report_pdf = file_
            record.data = record.parse_report(file_)
            if "error" in record.data:
                raise forms.ValidationError(record.data["error"])
            record.label = record.data.get("Defendant", {}).get("Name", "")
            if record.label and idx == 0:
                batch.label = record.label
                batch.save()
            record.refresh_record_from_data()
            offenses = record.data.get("Offense Record", {})
            if offenses:
                offense = Offense(
                    ciprs_record=record,
                    disposed_on=offenses.get("Disposed On", None),
                    disposition_method=offenses.get("Disposition Method", ""),
                )
                offense.save()
                offense_records = offenses.get("Records", [])
                for offense_record in offense_records:
                    o_record = OffenseRecord(
                        offense=offense,
                        law=offense_record.get("Law", ""),
                        # should 0 be the integer we store if Code is not given?
                        code=int(offense_record.get("Code", 0)),
                        action=offense_record.get("Action", ""),
                        severity=offense_record.get("Severity", ""),
                        description=offense_record.get("Description", ""),
                    )
                    o_record.save()
            batch.records.add(record)
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
