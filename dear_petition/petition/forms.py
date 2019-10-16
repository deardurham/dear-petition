import io
import os
import pdfrw
import dateutil.parser

from django import forms
from django.conf import settings

from dear_petition.petition.models import CIPRSRecord, Contact, Batch
from dear_petition.petition.writer import Writer
from dear_petition.petition.data_dict import map_data


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    def save(self):
        batch = Batch.objects.create()
        for file_ in self.files.getlist("files"):
            record = CIPRSRecord()
            if settings.CIPRS_SAVE_PDF:
                record.report_pdf = file_
            record.data = record.parse_report(file_)
            if "error" in record.data:
                raise forms.ValidationError(record.data["error"])
            if "Defendant" in record.data and "Name" in record.data["Defendant"]:
                record.label = record.data["Defendant"]["Name"]
            record.save()
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
            self.record.data.update(
                {
                    "NameAtty": data.name,
                    "StAddrAtty": data.address1,
                    "MailAddrAtty": data.address2,
                    "CityAtty": data.city,
                    "StateAtty": data.state,
                    "ZipCodeAtty": data.zipcode,
                }
            )
        return data

    def clean_agency1(self):
        data = self.cleaned_data["agency1"]
        if data:
            self.record.data.update(
                {
                    "NameAgency1": data.name,
                    "AddrAgency1": data.address1,
                    "MailAgency1": data.address2,
                    "CityAgency1": data.city,
                    "StateAgency1": data.state,
                    "ZipAgency1": data.zipcode,
                }
            )
        return data

    def clean_agency2(self):
        data = self.cleaned_data["agency2"]
        if data:
            self.record.data.update(
                {
                    "NameAgency2": data.name,
                    "AddrAgency2": data.address1,
                    "MailAgency2": data.address2,
                    "CityAgency2": data.city,
                    "StateAgency2": data.state,
                    "ZipAgency2": data.zipcode,
                }
            )
        return data

    def clean_dob(self):
        data = self.record.data
        try:
            dob = dateutil.parser.parse(
                data.get("Defendant", {}).get("Date of Birth/Estimated Age", "")
            )
        except ValueError:
            return
        cleaned_date = dob.date().strftime("%m/%d/%Y")
        self.record.data["Defendant"]["Date of Birth/Estimated Age"] = cleaned_date

    def clean_disposed_on_date(self):
        data = self.record.data
        try:
            date = dateutil.parser.parse(
                data.get("Offense Record", {}).get("Disposed On", "")
            )
        except ValueError:
            return
        cleaned_date = date.date().strftime("%m/%d/%Y")
        self.record.data["Offense Record"]["Disposed On"] = cleaned_date

    def clean_offense_date(self):
        data = self.record.data
        try:
            date = dateutil.parser.parse(
                data.get("Case Information", {}).get("Offense Date", "")
            )
        except ValueError:
            return
        cleaned_date = date.date().strftime("%m/%d/%Y")
        self.record.data["Case Information"]["Offense Date"] = cleaned_date

    def clean_offenses(self):
        offenses = self.record.data.get("Offense Record", {}).get("Records", [])
        if offenses:
            charged_offenses = []
            for offense in offenses:
                if offense["Action"].upper() == "CHARGED":
                    charged_offenses.append(offense)
            self.record.data["Offense Record"]["Records"] = charged_offenses

    def clean(self):
        # make sure checkbox is checked on PDF
        checked_box = pdfrw.PdfName("Yes")
        if "General" in self.record.data and "District" in self.record.data["General"]:
            self.record.data["General"]["District"] = checked_box
        if "General" in self.record.data and "Superior" in self.record.data["General"]:
            self.record.data["General"]["Superior"] = checked_box
        self.clean_dob()
        self.clean_disposed_on_date()
        self.clean_offense_date()
        self.clean_offenses()

    def save(self):
        output = io.BytesIO()
        template_path = os.path.join(
            settings.APPS_DIR, "static", "templates", "petition-template.pdf"
        )
        petition = Writer(self.record.data, map_data, template_path, output)
        petition.get_annotations()
        petition.write()
        output.seek(0)
        return output
