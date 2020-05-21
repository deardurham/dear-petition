import datetime as dt
import pytz
import pdfrw
import dateutil.parser

from django.conf import settings

from dear_petition.petition import constants
from dear_petition.petition.export.annotate import Checkbox
from dear_petition.petition.utils import dt_obj_to_date


def build_pdf_template_context(petition, extra):
    data = {}
    mappers = (map_petition, map_petitioner, map_attorney, map_agencies, map_offenses)
    for mapper in mappers:
        mapper(data, petition, extra)
    return data


def map_petition(data, petition, extra={}):
    data["County"] = getattr(petition, "county", None)
    jurisdiction = getattr(petition, "jurisdiction", None)
    if jurisdiction == constants.DISTRICT_COURT:
        data["District"] = Checkbox("Yes")
    else:
        data["District"] = Checkbox("")
    if jurisdiction == constants.SUPERIOR_COURT:
        data["Superior"] = Checkbox("Yes")
    else:
        data["Superior"] = Checkbox("")


def map_petitioner(data, petition, extra={}):
    record = petition.batch.most_recent_record
    data["NamePetitioner"] = getattr(
        record, "label", None
    )  # load.py line 28 (label is set to name attr)
    data["SSN"] = extra.get("ssn", None)
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
    data["NameAtty"] = getattr(attorney, "name", None)
    data["StAddrAtty"] = getattr(attorney, "address1", None)
    data["MailAddrAtty"] = getattr(attorney, "address2", None)
    data["CityAtty"] = getattr(attorney, "city", None)
    data["StateAtty"] = getattr(attorney, "state", None)
    data["ZipCodeAtty"] = getattr(attorney, "zipcode", None)
    ##### petition to expunge section ########
    # This section is signed by the Attorney
    ###########################################
    data["PetitionNotFiledSignName"] = getattr(attorney, "name", None)
    data["PetitionerAttorneyCbx"] = Checkbox("Yes")
    data["PetitionNotFiledSignDate"] = dt_obj_to_date(dt.datetime.today()).strftime(
        constants.DATE_FORMAT
    )


def map_agencies(data, petition, extra={}):
    agencies = extra.get("agencies", {})
    if agencies:
        agency1 = list(agencies)[0]
        data["NameAgency1"] = getattr(agency1, "name", None)
        data["AddrAgency1"] = getattr(agency1, "address1", None)
        data["MailAgency1"] = getattr(agency1, "address2", None)
        data["CityAgency1"] = getattr(agency1, "city", None)
        data["StateAgency1"] = getattr(agency1, "state", None)
        data["ZipAgency1"] = getattr(agency1, "zipcode", None)


def map_offenses(data, petition, extra={}):
    pass
