import abc
import datetime as dt

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
        method = offense.disposition_method
        return constants.DISPOSITION_METHOD_CODE_MAP.get(method.upper(), method)

    def get_ordered_offense_records(self):
        qs = self.petition.offense_records.select_related("offense__ciprs_record")
        return qs.order_by(
            "offense__ciprs_record__offense_date",
            "offense__ciprs_record__file_no",
            "pk",
        )

    @abc.abstractmethod
    def build_form_context(self):
        pass


class AOCFormCR287(PetitionForm):
    """
    Petition and Orders of Expunction Under G.S. 15A-146(a) and G.S. 15A-146(a1) (Charge(s) Dismissed)
    https://www.nccourts.gov/assets/documents/forms/cr287.pdf
    """

    def build_form_context(self):
        self.map_header()
        self.map_petitioner()

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

    def map_petitioner(self):
        # note: SNN and not SSN due to bug in PDF field name
        self.data["SNN"] = self.extra.get("ssn")
        self.data["DLNo"] = self.extra.get("drivers_license")
        self.data["DLState"] = self.extra.get("drivers_license_state")
        record = self.petition.batch.most_recent_record
        if record:
            self.data["NamePetitioner"] = record.label
            self.data["Race"] = record.race
            self.data["Sex"] = record.sex
            self.data["DOB"] = self.format_date(record.dob)
            self.data["ConsJdgmntFileNum"] = record.file_no

    def map_attorney(self):
        attorney = self.extra["attorney"]
        self.data["NameAtty"] = attorney.name
        self.data["StAddrAtty"] = attorney.address1
        self.data["MailAddrAtty"] = attorney.address2
        self.data["CityAtty"] = attorney.city
        self.data["StateAtty"] = attorney.state
        self.data["ZipCodeAtty"] = attorney.zipcode
        ##### petition to expunge section ########
        # This section is signed by the Attorney
        ###########################################
        self.data["PetitionNotFiledSignName"] = attorney.name
        self.data["PetitionerAttorneyCbx"] = Checkbox("Yes")
        self.data["PetitionNotFiledSignDate"] = self.format_date(dt.datetime.today())

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
            self.data[f"Disposition:{i}"] = self.disposition_code(offense)
            self.data[f"DispositionDate:{i}"] = self.format_date(offense.disposed_on)
