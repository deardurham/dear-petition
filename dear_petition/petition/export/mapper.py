import datetime as dt
import pytz
import pdfrw
import dateutil.parser

from django.conf import settings

from dear_petition.petition import constants


def transform_data(petition, extra):
    data = {}
    mappers = (map_petition, map_petitioner, map_attorney, map_agencies, map_offenses)
    for mapper in mappers:
        mapper(data, petition, extra)
    return data


def map_petition(data, petition, extra={}):
    data["County"] = petition.county
    data["District"] = (
        "Yes" if petition.jurisdiction == constants.DISTRICT_COURT else ""
    )
    data["Superior"] = (
        "Yes" if petition.jurisdiction == constants.SUPERIOR_COURT else ""
    )


def map_petitioner(data, petition, extra={}):
    pass


def map_attorney(data, petition, extra={}):
    pass


def map_agencies(data, petition, extra={}):
    pass


def map_offenses(data, petition, extra={}):
    pass


def old(form_data, batch):
    record = batch.most_recent_record
    # clean record data to fix date formats, etc.
    record = clean(record)
    json = record.data
    # add form data to json dict
    for data in form_data.values():
        if data:
            json.update(data)

    now = dt.datetime.now()
    now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).date()
    now = now.strftime("%m/%d/%Y")

    data = {
        "County": {"V": json.get("General", {}).get("County", "")},
        # File No
        "ConsJdgmntFileNum": {"V": json.get("General", {}).get("File No", "")},
        # Checkboxes: In The General Court of Justice
        "District": {"AS": json.get("General", {}).get("District", "")},
        "Superior": {"AS": json.get("General", {}).get("Superior", "")},
        # Name and Address of Petitioner
        "NamePetitioner": {"V": json.get("Defendant", {}).get("Name", "")},
        "StreetAddr": {"V": ""},
        "MailAddr": {"V": ""},
        "City": {"V": "Durham"},
        "State": {"V": "NC"},
        "ZipCode": {"V": "27701"},
        # Drivers License Number
        "DLNo": {"V": ""},
        "DLState": {"V": ""},
        # Race
        "Race": {"V": json.get("Defendant", {}).get("Race", "")},
        # Sex
        "Sex": {"V": json.get("Defendant", {}).get("Sex", "")},
        # Date of Birth
        "DOB": {"V": json.get("Defendant", {}).get("Date of Birth/Estimated Age", "")},
        # Full Social Security Number
        "SNN": {"V": ""},
        # Age At Time of Offense
        "Age": {"V": ""},
        # Name and Address of Petitioners Attorney
        "NameAtty": {"V": json.get("NameAtty", "")},
        "StAddrAtty": {"V": json.get("StAddrAtty", "")},
        "MailAddrAtty": {"V": json.get("MailAddrAtty", "")},
        "CityAtty": {"V": json.get("CityAtty", "")},
        "StateAtty": {"V": json.get("StateAtty", "")},
        "ZipCodeAtty": {"V": json.get("ZipCodeAtty", "")},
        # Agency 1
        "NameAgency1": {"V": json.get("NameAgency1", "")},
        "AddrAgency1": {"V": json.get("AddrAgency1", "")},
        "MailAgency1": {"V": json.get("MailAgency1", "")},
        "CityAgency1": {"V": json.get("CityAgency1", "")},
        "StateAgency1": {"V": json.get("StateAgency1", "")},
        "ZipAgency1": {"V": json.get("ZipAgency1", "")},
        # Agency 2
        "NameAgency2": {"V": json.get("NameAgency2", "")},
        "AddrAgency2": {"V": json.get("AddrAgency2", "")},
        "MailAgency2": {"V": json.get("MailAgency2", "")},
        "CityAgency2": {"V": json.get("CityAgency2", "")},
        "StateAgency2": {"V": json.get("StateAgency2", "")},
        "ZipAgency2": {"V": json.get("ZipAgency2", "")},
        # Petition to Expunge Section
        "PetitionNotFiledSignDate": {"V": now},
        "PetitionNotFiledSignName": {"V": json.get("NameAtty", "")},
        "PetitionerAttorneyCbx": {"AS": "Yes"},
    }

    data.update(batch.get_petition_offenses())
    return data


def clean_dob(record):
    data = record.data
    try:
        dob = dateutil.parser.parse(
            data.get("Defendant", {}).get("Date of Birth/Estimated Age", "")
        )
    except ValueError:
        return
    cleaned_date = dob.date().strftime("%m/%d/%Y")
    record.data["Defendant"]["Date of Birth/Estimated Age"] = cleaned_date


def clean_disposed_on_date(record):
    data = record.data
    try:
        date = dateutil.parser.parse(
            data.get("Offense Record", {}).get("Disposed On", "")
        )
    except ValueError:
        return
    cleaned_date = date.date().strftime("%m/%d/%Y")
    record.data["Offense Record"]["Disposed On"] = cleaned_date


def clean_offense_date(record):
    data = record.data
    try:
        date = dateutil.parser.parse(
            data.get("Case Information", {}).get("Offense Date", "")
        )
    except ValueError:
        return
    cleaned_date = date.date().strftime("%m/%d/%Y")
    record.data["Case Information"]["Offense Date"] = cleaned_date


def clean_arrest_date(record):
    data = record.data
    try:
        date = dateutil.parser.parse(
            data.get("Case Information", {}).get("Arrest Date", "")
        )
    except ValueError:
        return
    cleaned_date = date.date().strftime("%m/%d/%Y")
    record.data["Case Information"]["Arrest Date"] = cleaned_date


def clean_offenses(record):
    offenses = record.data.get("Offense Record", {}).get("Records", [])
    if offenses:
        charged_offenses = []
        for offense in offenses:
            if offense["Action"].upper() == "CHARGED":
                charged_offenses.append(offense)
        record.data["Offense Record"]["Records"] = charged_offenses


def clean(record):
    # make sure checkbox is checked on PDF
    checked_box = pdfrw.PdfName("Yes")
    if "General" in record.data and "District" in record.data["General"]:
        record.data["General"]["District"] = checked_box
    if "General" in record.data and "Superior" in record.data["General"]:
        record.data["General"]["Superior"] = checked_box
    clean_dob(record)
    clean_disposed_on_date(record)
    clean_offense_date(record)
    clean_arrest_date(record)
    clean_offenses(record)
    return record
