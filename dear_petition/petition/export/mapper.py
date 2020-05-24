import datetime as dt
import pytz
import pdfrw
import dateutil.parser

from django.conf import settings

from dear_petition.petition import constants
from dear_petition.petition import utils
from dear_petition.petition.export.annotate import Checkbox
from dear_petition.petition.utils import dt_obj_to_date


def build_pdf_template_context(petition, extra):
    data = {}
    mappers = (map_petition, map_petitioner, map_attorney, map_agencies, map_offenses)
    for mapper in mappers:
        mapper(data, petition, extra)
    return data


def map_petition(data, petition, extra={}):
    data["County"] = petition.county
    if petition.jurisdiction == constants.DISTRICT_COURT:
        data["District"] = Checkbox("Yes")
    else:
        data["District"] = Checkbox("")
    if petition.jurisdiction == constants.SUPERIOR_COURT:
        data["Superior"] = Checkbox("Yes")
    else:
        data["Superior"] = Checkbox("")


def map_petitioner(data, petition, extra={}):
    record = petition.batch.most_recent_record
    data["NamePetitioner"] = getattr(
        record, "label", None
    )  # load.py line 28 (label is set to name attr)
    # note: SNN and not SSN due to bug in PDF field name
    data["SNN"] = extra.get("ssn", None)
    data["DLNo"] = extra.get("drivers_license", None)
    data["DLState"] = extra.get("drivers_license_state", None)
    data["Race"] = getattr(record, "race", None)
    data["Sex"] = getattr(record, "sex", None)
    dob = getattr(record, "dob", None)
    if dob:
        data["DOB"] = dob.strftime(constants.DATE_FORMAT)
    # data["Age"] = getattr(record, "age", None)
    data["ConsJdgmntFileNum"] = getattr(record, "file_no", None)


def map_attorney(data, petition, extra={}):
    attorney = extra.get("attorney", None)
    data["NameAtty"] = attorney.name
    data["StAddrAtty"] = attorney.address1
    data["MailAddrAtty"] = attorney.address2
    data["CityAtty"] = attorney.city
    data["StateAtty"] = attorney.state
    data["ZipCodeAtty"] = attorney.zipcode
    ##### petition to expunge section ########
    # This section is signed by the Attorney
    ###########################################
    data["PetitionNotFiledSignName"] = attorney.name
    data["PetitionerAttorneyCbx"] = Checkbox("Yes")
    data["PetitionNotFiledSignDate"] = dt_obj_to_date(dt.datetime.today()).strftime(
        constants.DATE_FORMAT
    )


def map_agencies(data, petition, extra={}):
    agencies = extra.get("agencies", {})
    for idx, agency in enumerate(agencies, 1):
        data[f"NameAgency{idx}"] = agency.name
        data[f"AddrAgency{idx}"] = agency.address1
        data[f"MailAgency{idx}"] = agency.address2
        data[f"CityAgency1{idx}"] = agency.city
        data[f"StateAgency1{idx}"] = agency.state
        data[f"ZipAgency1{idx}"] = agency.zipcode


def map_offenses(data, petition, extra={}):
    offense_records = petition.get_offense_records()
    for idx, offense_record in enumerate(offense_records, 1):
        # The index of the offense determines what line on the petition form
        # the offense will be on
        data["Fileno:" + str(idx)] = offense_record.offense.ciprs_record.file_no
        data["ArrestDate:" + str(idx)] = utils.format_petition_date(
            offense_record.offense.ciprs_record.arrest_date
        )
        data["Description:" + str(idx)] = offense_record.description
        data["DOOF:" + str(idx)] = utils.format_petition_date(
            offense_record.offense.ciprs_record.offense_date
        )
        data["Disposition:" + str(idx)] = offense_record.offense.disposition_method
        data["DispositionDate:" + str(idx)] = utils.format_petition_date(
            offense_record.offense.disposed_on
        )
