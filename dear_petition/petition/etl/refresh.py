import logging
from dear_petition.petition import constants
from dear_petition.petition.utils import (
    dt_obj_to_date,
    make_datetime_aware,
)


logger = logging.getLogger(__name__)


def get_jurisdiction(record):
    is_superior = record.data.get("General", {}).get("Superior", "")
    is_district = record.data.get("General", {}).get("District", "")
    if is_superior:
        return constants.SUPERIOR_COURT
    elif is_district:
        return constants.DISTRICT_COURT
    else:
        return constants.NOT_AVAILABLE


def refresh_record_from_data(record, exclude_file_nos = []):
    """
    Transform record.data (JSONField) into model data.
    Refresh the CIPRS record from its JSON data. Optionally pass in a list of CIPRS record file numbers.
    If the list of file numbers contains the CIPRS record's file number, then the CIPRS record will not be saved.
    """
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

    if exclude_file_nos and record.file_no in exclude_file_nos:
        logger.warning(f"Not saving ciprs record {record.file_no} (most likely because it's a duplicate).")
        return

    logger.info(f"Saving ciprs record {record.file_no}")
    record.save()
    refresh_offenses(record)


def refresh_offenses(record):
    """Create Offense and OffenseRecords in each jurisdiction for this record."""
    for jurisdiction, header in constants.OFFENSE_HEADERS:
        offenses = record.data.get(header, {})

        # delete existing offenses in this jurisdiction
        record.offenses.filter(jurisdiction=jurisdiction).delete()
        for data_offense in offenses:
            offense = record.offenses.create(
                jurisdiction=jurisdiction,
                disposed_on=data_offense.get("Disposed On", None),
                disposition_method=data_offense.get("Disposition Method", ""),
                plea=data_offense.get("Plea", ""),
                verdict=data_offense.get("Verdict", ""),
            )
            for data_offense_record in data_offense.get("Records", []):
                offense.offense_records.create(
                    law=data_offense_record.get("Law", ""),
                    action=data_offense_record.get("Action", ""),
                    severity=data_offense_record.get("Severity", ""),
                    description=data_offense_record.get("Description", ""),
                )

            # update fields that are calculated from the values in other fields
            offense.update_is_visible()
            offense.update_disposition()
