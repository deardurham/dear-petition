import abc
import datetime as dt

from dear_petition.petition import constants, utils, models
from dear_petition.petition.export.annotate import Checkbox
from dear_petition.petition.utils import (
    get_285_form_agency_address,
    get_ordered_offense_records,
)


class PetitionForm(metaclass=abc.ABCMeta):
    def __init__(self, petition_document, extra={}):
        self.data = {}
        self.petition_document = petition_document
        self.petition = self.petition_document.petition
        self.extra = extra

    def format_date(self, date):
        return utils.format_petition_date(date)

    def disposition_code(self, offense):
        if offense.plea == "GUILTY TO LESSER":
            return "Glty to Lesser"
        method = offense.disposition_method
        return constants.DISPOSITION_METHOD_CODE_MAP.get(method.upper(), method)

    def get_ordered_offense_records(self):
        return get_ordered_offense_records(self.petition_document)

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
        self.data["ConsJdgmntFileNum"] = self.extra["file_no"]

    def map_petitioner(self):
        client = self.extra["client"]
        self.data["PetitionerName"] = client.name  # AOC-288
        self.data["NamePetitioner"] = client.name  # AOC-287
        self.data["StreetAddr"] = client.address1
        self.data["MailAddr"] = client.address2
        self.data["City"] = client.city
        self.data["State"] = client.state
        self.data["ZipCode"] = client.zipcode
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
        agencies = self.petition_document.agencies.all()
        assert (
            len(agencies) <= 3
        ), f"This form was given {len(agencies)} agencies. Three is the maximum."
        for i, agency in enumerate(agencies, 1):
            self.data[f"NameAgency{i}"] = agency.name
            self.data[f"AddrAgency{i}"] = agency.address1
            self.data[f"MailAgency{i}"] = agency.address2
            self.data[f"CityAgency{i}"] = agency.city
            self.data[f"{'Stateagency' if i==2 else 'StateAgency'}{i}"] = agency.state
            self.data[f"ZipAgency{i}"] = agency.zipcode

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
        if self.petition_document.form_specific_data.get("is_checkmark_3b_checked"):
            charged_desc_string = self.petition_document.form_specific_data.get(
                "charged_desc_string"
            )
            charged_desc_cont_string = self.petition_document.form_specific_data.get(
                "charged_desc_cont_string"
            )
            self.data["ChargedB"] = Checkbox("Yes")
            self.data["ChargedDesc"] = charged_desc_string
            self.data["ChargedDescCont"] = charged_desc_cont_string
        elif (
            self.petition.offense_records.filter(
                petitionoffenserecord__active=True
            ).count()
            > 1
        ):
            # Petition section says to check one of the checkboxes if petitioning to expunge MULTIPLE dismissals
            self.data["ChargedA"] = Checkbox("Yes")
        else:
            pass


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

    def map_header(self):
        super().map_header()
        self.data["CountyName"] = self.petition_document.county

    def map_file_no(self):
        self.data["FileNo"] = self.extra["file_no"]

    def map_petitioner(self):
        client = self.extra["client"]
        self.data["PetitionerName"] = client.name

    def map_agencies(self):
        agencies = self.petition_document.agencies.all()
        assert (
            len(agencies) <= 3
        ), f"This form was given {len(agencies)} Three is the maximum."
        if len(agencies) > 0:
            self.data["FormNo1"] = self.petition_document.petition.form_type.split("-")[
                -1
            ]
        for i, agency in enumerate(agencies, 1):
            body = get_285_form_agency_address(agency)
            self.data[f"NameAddress{i}"] = body

    def map_offenses(self):
        self.data["FormNo2"] = self.petition_document.petition.form_type.split("-")[-1]
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


class AOCFormCR293(AOCFormCR287):
    pass


class AOCFormCR297(AOCFormCR287):
    def map_file_no(self):
        self.data["FileNumber"] = self.extra["file_no"]

    def map_header(self):
        self.data["County"] = self.petition.county
        if self.petition.jurisdiction == constants.DISTRICT_COURT:
            self.data["DistrictCourtDivisionCkBox"] = Checkbox("Yes")
        else:
            self.data["DistrictCourtDivisionCkBox"] = Checkbox("")
        if self.petition.jurisdiction == constants.SUPERIOR_COURT:
            self.data["SuperiorCourtDivisionCkBox"] = Checkbox("Yes")
        else:
            self.data["SuperiorCourtDivisionCkBox"] = Checkbox("")

    def map_offenses(self):
        offense_records = self.get_ordered_offense_records()
        for i, offense_record in enumerate(offense_records, 1):
            offense = offense_record.offense
            ciprs_record = offense.ciprs_record
            # The index of the offense determines what line on the petition form
            # the offense will be on
            self.data[f"FileNumber:{i}"] = ciprs_record.file_no
            self.data[f"ArrestDate:{i}"] = self.format_date(ciprs_record.arrest_date)
            self.data[f"OffenseDescription:{i}"] = offense_record.description
            self.data[f"Disposition:{i}"] = self.format_date(ciprs_record.offense_date)
            self.data[f"DispositionDate:{i}"] = self.format_date(offense.disposed_on)

    def map_petitioner(self):
        client = self.extra["client"]
        self.data["PetitionerName"] = client.name  # AOC-288
        self.data["PetitionerStreetAddress"] = client.address1
        self.data["PetitionerMailAddress"] = client.address2
        self.data["PetitionerCity"] = client.city
        self.data["PetitionerState"] = client.state
        self.data["PetitionerZip"] = client.zipcode
        offense_record = self.get_most_recent_record()
        if offense_record:
            record = offense_record.offense.ciprs_record
            self.data["Race"] = record.race
            self.data["Sex"] = record.sex
            self.data["DOB"] = self.format_date(record.dob)

    def map_additional_forms(self):
        if (
            self.petition.offense_records.filter(
                petitionoffenserecord__active=True
            ).count()
            > 1
        ):
            # Petition section says to check one of the checkboxes if petitioning to expunge MULTIPLE dismissals
            self.data["TwoOrThreeNonviolentFeloniesWaitingPeriodCkBox"] = Checkbox(
                "Yes"
            )
        else:
            self.data["OneNonviolentFelonyWaitingPeriodCkBox"] = Checkbox("Yes")

    def map_attorney(self):
        attorney = self.extra["attorney"]
        self.data["AttorneyName"] = attorney.name
        self.data["AttorneyStreetAddress"] = attorney.address1
        self.data["AttorneyMailAddress"] = attorney.address2
        self.data["AttorneyCity"] = attorney.city
        self.data["AttorneyState"] = attorney.state
        self.data["AttorneyZip"] = attorney.zipcode
        #
        # Petition to expunge section
        #
        self.data["PetitionerPetitionersAttorneySignedName"] = attorney.name
        self.data["PetitionersAttorneyCkBox"] = Checkbox("Yes")
        self.data["PetitionerPetitionersAttorneySignedDate"] = self.format_date(
            dt.datetime.today()
        )


class AOCFormCR298(AOCFormCR297):
    pass
