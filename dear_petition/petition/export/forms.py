import abc
import datetime as dt

from django.db.models import IntegerField, Case, When, Value
from django.db.models.functions import Cast, Substr, Concat
from django.utils import timezone

from dear_petition.petition import constants, utils
from dear_petition.petition.export.annotate import Checkbox


class PetitionForm(metaclass=abc.ABCMeta):
    def __init__(self, petition, extra={}):
        self.data = {}
        self.petition = petition
        self.extra = extra

    def format_date(self, date):
        return utils.format_petition_date(date)

    def disposition_code(self, offense):
        if offense.plea == "GUILTY TO LESSER":
            return "Glty to Lesser"
        method = offense.disposition_method
        return constants.DISPOSITION_METHOD_CODE_MAP.get(method.upper(), method)

    def get_ordered_offense_records(self):
        # When sorting these, need to interpret first 2 digits of file number as year and sort based on that
        two_digit_current_year = timezone.now().year % 2000 #Returns 21 given 2021
        qs = self.petition.offense_records.select_related("offense__ciprs_record").annotate(
            first_two_digits_file_number_chars = Substr("offense__ciprs_record__file_no", 1, 2)
        ).annotate(
            first_two_digits_file_number = Cast('first_two_digits_file_number_chars', output_field=IntegerField())
        ).annotate(
            file_number_year = Case(
                When(first_two_digits_file_number__gt=two_digit_current_year, then=Concat(Value("19"),"first_two_digits_file_number_chars")),
                When(first_two_digits_file_number__lte=two_digit_current_year, then=Concat(Value("20"),"first_two_digits_file_number_chars")),
            )
        ).order_by(
            "file_number_year",
            "pk",            
        )
        return qs

    def get_most_recent_record(self):
        return self.get_ordered_offense_records().last()

    @abc.abstractmethod
    def build_form_context(self):
        pass


class DataPetitionForm(PetitionForm):
    """A basic form that renders from a context dictionary."""

    def build_form_context(self):
        self.data = self.extra


class AOCFormCR287(PetitionForm):
    """
    Petition and Orders of Expunction Under G.S. 15A-146(a) and G.S. 15A-146(a1) (Charge(s) Dismissed)
    https://www.nccourts.gov/assets/documents/forms/cr287.pdf
    """

    MULTIPLE_FILE_NO_MSG = "Multiple - See Below"

    def build_form_context(self):
        self.map_file_no()
        self.map_header()
        self.map_petitioner()
        self.map_attorney()
        self.map_agencies()
        self.map_offenses()
        self.map_additional_forms()

    def map_header(self):
        self.data["County"] = self.petition.county
        if self.petition.jurisdiction == constants.DISTRICT_COURT:
            self.data["District"] = Checkbox("Yes")
        else:
            self.data["District"] = Checkbox("")
        if self.petition.jurisdiction == constants.SUPERIOR_COURT:
            self.data["Superior"] = Checkbox("Yes")
        else:
            self.data["Superior"] = Checkbox("")

    def map_file_no(self):
        if self.petition.offense_records.count() > 1:
            self.data["ConsJdgmntFileNum"] = self.MULTIPLE_FILE_NO_MSG
        else:
            offense_record = self.get_most_recent_record()
            if offense_record:
                self.data[
                    "ConsJdgmntFileNum"
                ] = offense_record.offense.ciprs_record.file_no

    def map_petitioner(self):
        self.data["PetitionerName"] = self.extra.get("name_petitioner") #AOC-288
        self.data["NamePetitioner"] = self.extra.get("name_petitioner") #AOC-287
        self.data["StreetAddr"] = self.extra.get("address1")
        self.data["MailAddr"] = self.extra.get("address2")
        self.data["City"] = self.extra.get("city")
        self.data["State"] = self.extra.get("state")
        self.data["ZipCode"] = self.extra.get("zip_code")
        # note: SNN and not SSN due to bug in PDF field name
        self.data["SNN"] = self.extra.get("ssn")
        self.data["DLNo"] = self.extra.get("drivers_license")
        self.data["DLState"] = self.extra.get("drivers_license_state")
        offense_record = self.get_most_recent_record()
        if offense_record:
            record = offense_record.offense.ciprs_record
            self.data["NamePetitioner"] = record.label
            self.data["Race"] = record.race
            self.data["Sex"] = record.sex
            self.data["DOB"] = self.format_date(record.dob)

    def map_attorney(self):
        attorney = self.extra["attorney"]
        self.data["NameAtty"] = attorney.name
        self.data["StAddrAtty"] = attorney.address1
        self.data["MailAddrAtty"] = attorney.address2
        self.data["CityAtty"] = attorney.city
        self.data["StateAtty"] = attorney.state
        self.data["ZipCodeAtty"] = attorney.zipcode
        #
        # Petition to expunge section
        #
        self.data["PetitionNotFiledSignName"] = attorney.name
        self.data["PetitionerAttorneyCbx"] = Checkbox("Yes")
        self.data["PetitionNotFiledSignDate"] = self.format_date(dt.datetime.today())

    def map_agencies(self):
        agencies = self.extra.get("agencies", [])
        for i, agency in enumerate(agencies, 1):
            self.data[f"NameAgency{i}"] = agency.name
            self.data[f"AddrAgency{i}"] = agency.address1
            self.data[f"MailAgency{i}"] = agency.address2
            self.data[f"CityAgency1{i}"] = agency.city
            self.data[f"StateAgency1{i}"] = agency.state
            self.data[f"ZipAgency1{i}"] = agency.zipcode

    def map_offenses(self):
        offense_records = self.get_ordered_offense_records()
        for i, offense_record in enumerate(offense_records, 1):
            offense = offense_record.offense
            ciprs_record = offense.ciprs_record
            # The index of the offense determines what line on the petition form
            # the offense will be on
            self.data[f"Fileno:{i}"] = ciprs_record.file_no
            self.data[f"ArrestDate:{i}"] = self.format_date(ciprs_record.arrest_date)
            self.data[f"Description:{i}"] = offense_record.description
            self.data[f"DOOF:{i}"] = self.format_date(ciprs_record.offense_date)
            self.data[f"DismissalDate:{i}"] = self.format_date(offense.disposed_on)

    def map_additional_forms(self):
        if self.petition.has_attachments():
            self.data["CkBox_Attchmt"] = Checkbox("Yes")


class AOCFormCR285(AOCFormCR287):
    """
    Expunction Petition Attachment: Additional Agencies/Additional File Nos. And Offenses

    https://www.nccourts.gov/assets/documents/forms/cr285-en.pdf
    """

    MULTIPLE_FILE_NO_MSG = "Multiple - See Petition and Below"

    def build_form_context(self):
        self.map_file_no()
        self.map_header()
        self.map_petitioner()
        self.map_agencies()
        self.map_offenses()

    def map_file_no(self):
        self.data["FileNo"] = self.MULTIPLE_FILE_NO_MSG

    def map_header(self):
        super().map_header()
        self.data["CountyName"] = self.petition.county

    def map_petitioner(self):
        self.data["PetitionerName"] = self.extra.get("name_petitioner")

    def map_agencies(self):
        agencies = self.extra.get("agencies", [])
        if len(agencies) > 0:
            self.data["FormNo1"] = self.petition.parent.form_type.split("-")[-1]
        for i, agency in enumerate(agencies, 1):
            body = ""
            for field_name in [
                "name",
                "address1",
                "address2",
                "city",
                "state",
                "zipcode",
            ]:
                field = getattr(agency, field_name)
                body += f"{field}\n"
            self.data[f"NameAddress{i}"] = body

    def map_offenses(self):
        self.data["FormNo2"] = self.petition.parent.form_type.split("-")[-1]
        for i, offense_record in enumerate(self.get_ordered_offense_records(), 1):
            row = {}
            offense = offense_record.offense
            ciprs_record = offense.ciprs_record
            row[f"FileNoRow{i}"] = ciprs_record.file_no
            row[f"ArrestDateRow{i}"] = self.format_date(ciprs_record.arrest_date)
            row[f"OffenseDescRow{i}"] = offense_record.description
            row[f"DateOfOffenseRow{i}"] = self.format_date(ciprs_record.offense_date)
            row[f"DispositionRow{i}"] = self.disposition_code(offense)
            row[f"DispositionDateRow{i}"] = self.format_date(offense.disposed_on)
            self.data.update(row)


class AOCFormCR288(AOCFormCR287):
    def map_offenses(self):
        offense_records = self.get_ordered_offense_records()
        for i, offense_record in enumerate(offense_records, 1):
            offense = offense_record.offense
            ciprs_record = offense.ciprs_record
            # The index of the offense determines what line on the petition form
            # the offense will be on
            self.data[f"Fileno:{i}"] = ciprs_record.file_no
            self.data[f"ArrestDate:{i}"] = self.format_date(ciprs_record.arrest_date)
            self.data[f"Description:{i}"] = offense_record.description
            self.data[f"DOOF:{i}"] = self.format_date(ciprs_record.offense_date)
            self.data[f"Disposition:{i}"] = "NOT GUILTY"
            self.data[f"DispositionDate:{i}"] = self.format_date(offense.disposed_on)
