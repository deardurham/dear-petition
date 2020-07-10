import datetime as dt

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
    data[petition.form_field("County")] = petition.county
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
    data[petition.form_field("NamePetitioner")] = record.label
    # note: SNN and not SSN due to bug in PDF field name
    data["SNN"] = extra.get("ssn", None)
    data["DLNo"] = extra.get("drivers_license", None)
    data["DLState"] = extra.get("drivers_license_state", None)
    data["Race"] = getattr(record, "race", None)
    data["Sex"] = getattr(record, "sex", None)
    dob = getattr(record, "dob", None)
    if dob:
        data["DOB"] = dob.strftime(constants.DATE_FORMAT)
    data[petition.form_field("FileNo")] = record.file_no


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
    # AOC-CR-285
    if petition.parent:
        data["FormNo1"] = petition.parent.form_type.split("-")[-1]


def map_offenses(data, petition, extra={}):
    offense_records = petition.offense_records.all()
    for idx, offense_record in enumerate(offense_records, 1):
        file_no_field = petition.form_field("OffenseFileNoRow").format(idx=idx)
        arrest_date_field = petition.form_field("OffenseArrestDateRow").format(idx=idx)
        description_field = petition.form_field("OffenseDescriptionRow").format(idx=idx)
        doof_field = petition.form_field("OffenseDOOFRow").format(idx=idx)
        disposition_field = petition.form_field("OffenseDispositionRow").format(idx=idx)
        disposition_date_field = petition.form_field(
            "OffenseDispositionDateRow"
        ).format(idx=idx)
        # The index of the offense determines what line on the petition form
        # the offense will be on
        offense = offense_record.offense
        ciprs_record = offense.ciprs_record
        data[file_no_field] = ciprs_record.file_no
        data[arrest_date_field] = utils.format_petition_date(ciprs_record.arrest_date)
        data[description_field] = offense_record.description
        data[doof_field] = utils.format_petition_date(ciprs_record.offense_date)
        data[disposition_field] = constants.DISPOSITION_METHOD_CODE_MAP.get(
            offense.disposition_method.upper(), offense.disposition_method,
        )
        data[disposition_date_field] = utils.format_petition_date(offense.disposed_on)
    # AOC-CR-285
    if petition.parent:
        data["FormNo2"] = petition.parent.form_type.split("-")[-1]
