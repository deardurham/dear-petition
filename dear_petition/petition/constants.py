from collections import defaultdict

from model_utils import Choices

DISTRICT_COURT = "D"
SUPERIOR_COURT = "S"
NOT_AVAILABLE = "N/A"

JURISDICTION_CHOICES = Choices(
    (DISTRICT_COURT, "DISTRICT COURT"),
    (SUPERIOR_COURT, "SUPERIOR COURT"),
    (NOT_AVAILABLE, "NOT AVAILABLE"),
)

OFFENSE_HEADERS = Choices(
    (DISTRICT_COURT, "District Court Offense Information"),
    (SUPERIOR_COURT, "Superior Court Offense Information"),
)

MALE = "M"
FEMALE = "F"
UNKNOWN = "U"
SEX_CHOICES = Choices(
    (MALE, "Male"),
    (FEMALE, "Female"),
    (UNKNOWN, "Unknown"),
    (NOT_AVAILABLE, "NOT AVAILABLE"),
)

CONTACT_CATEGORIES = Choices(("agency", "Agency"), ("attorney", "Attorney"))

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

CHARGED = "CHARGED"
CONVICTED = "CONVICTED"
ARRAIGNED = "ARRAIGNED"

COMMENT_MAX_LENGTH = 8192

NEW_COMMENT_EMAIL_SUBJECT = "New comment available for batch #{batch}"
NEW_COMMENT_EMAIL_MESSAGE = "There is a new comment available for batch#{batch}.{user}\n\n\n{text}\n\nSee it here:{link}"

DATA_PETITION = "DATA-PETITION"

MISDEMEANOR = "AOC-CR-281"
ATTACHMENT = "AOC-CR-285"
DISMISSED = "AOC-CR-287"
NOT_GUILTY = "AOC-CR-288"
UNDERAGED_CONVICTIONS = "AOC-CR-293"
FORM_TYPES = (
    (MISDEMEANOR, MISDEMEANOR),
    (ATTACHMENT, ATTACHMENT),
    (DISMISSED, DISMISSED),
    (NOT_GUILTY, NOT_GUILTY),
    (UNDERAGED_CONVICTIONS, UNDERAGED_CONVICTIONS),
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
    "Deferred Proceeding or Deferred Prosecution Dismissal",
)

DISPOSITION_METHOD_CODE_MAP = {
    "DISMISSAL WITHOUT LEAVE BY DA": "VD",
    "DISMISSED BY COURT": "DC",
    "DEFERRED PROSECUTION DISMISSAL": "DPD",
    "DISCHARGE AND DISMISSAL": "DD",
    "CONDITIONAL DISCHARGE": "DD",
    "NO PROBABLE CAUSE": "NPC",
    "NEVER TO BE SERVED": "NTBS",
    "DEFERRED PROCEEDING OR DEFERRED PROSECUTION DISMISSAL": "DPD",
}
