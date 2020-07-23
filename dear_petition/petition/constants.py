from collections import defaultdict

DISTRICT_COURT = "D"
SUPERIOR_COURT = "S"
NOT_AVAILABLE = "N/A"

JURISDICTION_CHOICES = (
    (DISTRICT_COURT, "DISTRICT COURT"),
    (SUPERIOR_COURT, "SUPERIOR COURT"),
    (NOT_AVAILABLE, "NOT AVAILABLE"),
)

OFFENSE_HEADERS = (
    (DISTRICT_COURT, "District Court Offense Information"),
    (SUPERIOR_COURT, "Superior Court Offense Information"),
)

MALE = "M"
FEMALE = "F"
UNKNOWN = "U"
SEX_CHOICES = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (UNKNOWN, "Unknown"),
    (NOT_AVAILABLE, "NOT AVAILABLE"),
)

CONTACT_CATEGORIES = (("agency", "Agency"), ("attorney", "Attorney"))

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

CHARGED = "CHARGED"
ARRAIGNED = "ARRAIGNED"

COMMENT_MAX_LENGTH = 8192

NEW_COMMENT_EMAIL_SUBJECT = "New comment available for batch #{batch}"
NEW_COMMENT_EMAIL_MESSAGE = "There is a new comment available for batch#{batch}.{user}\n\n\n{text}\n\nSee it here:{link}"


MISDEMEANOR = "AOC-CR-281"
ATTACHMENT = "AOC-CR-285"
DISMISSED = "AOC-CR-287"
NOT_GUILTY = "AOC-CR-288"
FORM_TYPES = (
    (MISDEMEANOR, MISDEMEANOR),
    (ATTACHMENT, ATTACHMENT),
    (DISMISSED, DISMISSED),
    (NOT_GUILTY, NOT_GUILTY),
)

NORTH_CAROLINA = "NC"
DURHAM_COUNTY = "DURHAM"

DISTRICT_COURT_WITHOUT_DA_LEAVE = "Dismissal without Leave by DA"

DISMISSED_DISPOSITION_METHODS = (
    DISTRICT_COURT_WITHOUT_DA_LEAVE,
    "Dismissed by Court",
    "Deferred Prosecution Dismissal",
    "Discharge and Dismissal",
    "Conditional Discharge",
    "No Probable Cause",
    "Never To Be Served",
)

DISPOSITION_METHOD_CODE_MAP = {
    "DISMISSAL WITHOUT LEAVE BY DA": "VD",
    "DISMISSED BY COURT": "DC",
    "DEFERRED PROSECUTION DISMISSAL": "DPD",
    "DISCHARGE AND DISMISSAL": "DD",
    "CONDITIONAL DISCHARGE": "DD",
    "NO PROBABLE CAUSE": "NPC",
    "NEVER TO BE SERVED": "NTBS",
    "GUILTY TO LESSER": "Glty to Lesser",
}
