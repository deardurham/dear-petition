from dear_petition.petition import constants
from dear_petition.petition.utils import (
    dt_obj_to_date,
    make_datetime_aware,
)


def get_jurisdiction(record):
    is_superior = record.data.get("General", {}).get("Superior", "")
    is_district = record.data.get("General", {}).get("District", "")
    if is_superior:
        return constants.SUPERIOR_COURT
    elif is_district:
        return constants.DISTRICT_COURT
    else:
        return constants.NOT_AVAILABLE


def refresh_record_from_data(record):
    """Transform record.data (JSONField) into model data."""
    record.label = record.data.get("Defendant", {}).get("Name", "")
    record.file_no = record.data.get("General", {}).get("File No", "")
    record.county = record.data.get("General", {}).get("County", "")
    record.dob = record.data.get("Defendant", {}).get(
        "Date of Birth/Estimated Age", None
    )
    record.sex = record.data.get("Defendant", {}).get("Sex", constants.NOT_AVAILABLE)
    record.race = record.data.get("Defendant", {}).get("Race", "")
    record.case_status = record.data.get("Case Information", {}).get("Case Status", "")
    record.offense_date = make_datetime_aware(
        record.data.get("Case Information", {}).get("Offense Date", None)
    )
    record.arrest_date = record.data.get("Case Information", {}).get(
        "Arrest Date", dt_obj_to_date(record.offense_date)
    )
    record.jurisdiction = get_jurisdiction(record)
    record.save()

    # import both District and Superior court offenses
    for jurisdiction, header in constants.OFFENSE_HEADERS:
        offenses = record.data.get(header, {})
        refresh_offenses(record, jurisdiction, offenses)


def refresh_offenses(record, jurisdiction, offenses):
    """Create Offense and OffenseRecords in jurisdiction for this record."""
    # delete existing offenses in this jurisdiction
    record.offenses.filter(jurisdiction=jurisdiction).delete()
    for data_offense in offenses:
        offense = record.offenses.create(
            jurisdiction=jurisdiction,
            disposed_on=data_offense.get("Disposed On", None),
            disposition_method=data_offense.get("Disposition Method", ""),
        )
        for data_offense_record in data_offense.get("Records", []):
            offense.offense_records.create(
                law=data_offense_record.get("Law", ""),
                action=data_offense_record.get("Action", ""),
                severity=data_offense_record.get("Severity", ""),
                description=data_offense_record.get("Description", ""),
            )
