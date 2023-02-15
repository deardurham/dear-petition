from django.conf import settings
from docxtpl import DocxTemplate
from dateutil.relativedelta import relativedelta

from dear_petition.petition import models as pm
from dear_petition.petition.constants import (
    DISPOSITION_METHOD_CODE_MAP,
    JURISDICTION_MAP,
    SUPERSEDING_INDICTMENT_OR_PROCESS
)

TEMPLATE = "expungable_summary.docx"


def generate_expungable_summary(batch, contact, petitioner_info):

    context = generate_context(batch, contact, petitioner_info)
    doc = DocxTemplate(settings.TEMPLATE_DIR.path(TEMPLATE))
    doc.render(context)

    return doc


def generate_context(batch, contact, petitioner_info):

    dob = batch.dob
    birthday_18th = "None"
    birthday_22nd = "None"

    # if born in leap year, add one day so birthdays will be on March 1
    leap_year_adjustment = 1 if dob.month == 2 and dob.day == 29 else 0

    if dob:
        birthday_18th = dob + relativedelta(years=18, days=leap_year_adjustment)
        birthday_22nd = dob + relativedelta(years=22, days=leap_year_adjustment)

    # tables_data is a dictionary where the key is a (county, jurisdiction) tuple and the value is a list of offense
    # records for that county and jurisdiction
    tables_data: dict[tuple[str, str], list] = __get_tables_data(batch)
    tables_keys = list(tables_data.keys())
    # sort tables first by county, then by jurisdiction
    tables_keys.sort()
    tables = []
    for i, k in enumerate(tables_keys, start=1):
        offense_records = tables_data[k]
        # sort offense records by file number
        offense_records.sort(key=lambda x: x["file_no"])
        table = {"county": k[0], "jurisdiction": k[1], "idx": i , "offense_records": offense_records}
        tables.append(table)

    return {
        "attorney": contact.name,
        "petitioner": petitioner_info["name"],
        "dob": dob,
        "birthday_18th": birthday_18th,
        "birthday_22nd": birthday_22nd,
        "tables": tables,
    }


def __get_tables_data(batch):
    """
    Organize offense records into a dictionary where the key is a (county, jurisdiction) tuple and the value is a list
    of offense records for that county and jurisdiction. Exclude offense records that have an offense with a disposition
    "SUPERSEDING INDICTMENT OR PROCESS".
    """

    offense_records = pm.OffenseRecord.objects.filter(
        offense__ciprs_record__batch=batch
    ).exclude(
        offense__disposition_method=SUPERSEDING_INDICTMENT_OR_PROCESS
    ).select_related("offense__ciprs_record__batch")

    table_data = {}

    for offense_record in offense_records:
        county = offense_record.offense.ciprs_record.county
        jurisdiction = JURISDICTION_MAP[offense_record.offense.ciprs_record.jurisdiction]
        key = (county, jurisdiction)

        severity = offense_record.severity
        offense_date = offense_record.offense.ciprs_record.offense_date
        offense_record_data = {
            "file_no": offense_record.file_no,
            "arrest_date": offense_record.offense.ciprs_record.arrest_date,
            "description": offense_record.description,
            "severity": severity[0:1] if severity else None,
            "offense_date": offense_date.strftime("%Y-%m-%d") if offense_date else None,
            # if can't get disposition method abbreviation from map, then use disposition method (not the abbreviation)
            "disposition_method": DISPOSITION_METHOD_CODE_MAP.get(
                offense_record.offense.disposition_method,
                offense_record.offense.disposition_method
            ),
            "disposed_on": offense_record.disposed_on
        }

        # append offense record to list for the key, but if key doesn't exist yet, create an empty list first
        table_data.setdefault(key, []).append(offense_record_data)

    return table_data
