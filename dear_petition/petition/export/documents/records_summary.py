import logging
from django.conf import settings
from docxtpl import DocxTemplate
from dateutil.relativedelta import relativedelta

from dear_petition.petition import utils
from dear_petition.petition import models as pm
from dear_petition.petition.constants import (
    DISPOSITION_METHOD_CODE_MAP,
    VERDICT_CODE_MAP,
    JURISDICTION_MAP,
)


logger = logging.getLogger(__name__)

TEMPLATE = "records_summary.docx"


def generate_summary(batch):
    assert (
        batch.client is not None and batch.attorney is not None
    ), "Client and attorney must be set for batch before generating document"

    context = generate_context(batch, batch.attorney, batch.client)
    doc = DocxTemplate(settings.TEMPLATE_DIR.path(TEMPLATE))
    doc.render(context)

    return doc


def generate_context(batch, attorney, client):
    dob = batch.dob
    birthday_18th = "None"
    birthday_22nd = "None"

    """
    If born in leap year, add one day so 18th and 22nd birthdays will be on March 1. Note that birthdays that are
    divisible by 4 (eg 20th, 24th birthday) would not be adjusted if we ever calculate them. They would fall on a leap
    year, so the birthday would be on February 29.
    """
    leap_year_adjustment = 1 if dob and dob.month == 2 and dob.day == 29 else 0

    if dob:
        birthday_18th = dob + relativedelta(years=18, days=leap_year_adjustment)
        birthday_22nd = dob + relativedelta(years=22, days=leap_year_adjustment)

    # tables_data is a dictionary where the key is a (county, jurisdiction) tuple and the value is a list of offense
    # records for that county and jurisdiction
    offenses = __get_offenses(batch)
    tables_data: dict[tuple[str, str], list] = __create_tables_data(offenses)
    tables_keys = list(tables_data.keys())
    # sort tables first by county, then by jurisdiction
    tables_keys.sort()
    tables = []
    for table_index, table_key in enumerate(tables_keys, start=1):
        # get offense records for county and jurisdiction
        offense_records = tables_data[table_key]

        # sort offense records by file number
        offense_records.sort(key=lambda x: x["file_no"])

        # assign index for each offense record and create set of file numbers with "additional offenses exist"
        addl_offense_file_nos = set()
        for offense_record_index, offense_record in enumerate(offense_records, start=1):
            offense_record["idx"] = offense_record_index
            if offense_record["has_additional_offenses"]:
                addl_offense_file_nos.add(offense_record["file_no"])

        table = {
            "county": table_key[0],
            "jurisdiction": table_key[1],
            "idx": table_index,
            "offense_records": offense_records,
            "addl_offense_file_nos": ", ".join(sorted(addl_offense_file_nos)),
        }
        tables.append(table)

    return {
        "attorney": attorney.name,
        "petitioner": client.name,
        "dob": __format_date(dob),
        "birthday_18th": __format_date(birthday_18th),
        "birthday_22nd": __format_date(birthday_22nd),
        "tables": tables,
    }


def __get_offenses(batch):
    """
    Get offenses for the batch.
    """
    offenses = pm.Offense.objects.filter(ciprs_record__batch=batch).select_related(
        "ciprs_record__batch"
    )

    return offenses


def __create_tables_data(offenses):
    """
    Create the data that populates the offense record tables in the document. Organize offense records into a
    dictionary where the key is a (county, jurisdiction) tuple and the value is a list of offense records for that county
    and jurisdiction.
    """
    table_data = {}

    for offense in offenses:
        county = offense.ciprs_record.county
        jurisdiction = JURISDICTION_MAP[offense.jurisdiction]
        key = (county, jurisdiction)

        offense_records = list(offense.offense_records.all())

        for offense_record in offense_records:
            if not offense_record.is_visible:
                continue

            offense_record_data = __create_offense_record_data(offense_record)

            # append offense record data to list for the key, but if key doesn't exist yet, create an empty list first
            table_data.setdefault(key, []).append(offense_record_data)

    return table_data


def __create_offense_record_data(offense_record):
    """
    Create the data that populates the offense record row in the document.
    """
    offense = offense_record.offense
    ciprs_record = offense.ciprs_record

    """
    First try to get disposition code from disposition method code map and if that fails, then try verdict code
    map. If that fails, use disposition (not the abbreviation).
    """
    disposition = DISPOSITION_METHOD_CODE_MAP.get(
        offense_record.disposition,
        VERDICT_CODE_MAP.get(offense_record.disposition, offense_record.disposition),
    )

    offense_record_data = {
        "file_no": ciprs_record.file_no,
        "arrest_date": __format_date(ciprs_record.arrest_date),
        "description": offense_record.description,
        "severity": offense_record.severity[0:1] if offense_record.severity else None,
        "offense_date": __format_date(ciprs_record.offense_date),
        "disposition": disposition,
        "disposed_on": __format_date(offense.disposed_on),
        "has_additional_offenses": ciprs_record.has_additional_offenses,
    }

    return offense_record_data


def __format_date(date):
    """
    Format the date for the Summary Document.
    """
    return utils.format_petition_date(date)
