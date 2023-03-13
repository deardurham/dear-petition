from model_utils import Choices

DISTRICT_COURT = "D"
SUPERIOR_COURT = "S"
NOT_AVAILABLE = "N/A"

JURISDICTION_MAP = {
    DISTRICT_COURT: "DISTRICT COURT",
    SUPERIOR_COURT: "SUPERIOR COURT",
    NOT_AVAILABLE: "NOT AVAILABLE"
}

JURISDICTION_CHOICES = Choices(*[(k, v) for k, v in JURISDICTION_MAP.items()])

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
FORM_TYPES = Choices(
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

DISP_SUPERSEDING_INDICTMENT = "SUPERSEDING INDICTMENT OR PROCESS"

DISPOSITION_METHOD_CODE_MAP = {
    "APPEAL WITHDRAWN FROM SUPERIOR COURT": "WD",
    "CHANGE OF VENUE": "CV",
    "CONDITIONAL DISCHARGE": "DD",
    "DEFERRED PROCEEDING OR DEFERRED PROSECUTION DISMISSAL": "DPD",
    "DEFERRED PROSECUTION DISMISSAL": "DPD",
    "DISCHARGE AND DISMISSAL": "DD",
    "DISMISSED BY COURT": "DC",
    "DISMISSAL WITH LEAVE BY DA": "VL",
    "DISMISSAL WITHOUT LEAVE BY DA": "VD",
    "DISMISSED BY DA - SPEEDY TRIAL": "ST",
    "DISPOSED BY JUDGE": "GU",
    "FIGHT EXTRADITION": "FE",
    "HABEAS CORPUS HEARING": "HC",
    "JUDGE": "JU",
    "JURY TRIAL": "JR",
    "MAGISTRATE": "MA",
    "NEVER TO BE SERVED": "NTBS",
    "NO PROBABLE CAUSE": "NPC",
    "NO TRUE BILL RETURNED": "NB",
    "OTHER": "OT",
    "PROBABLE CAUSE FOUND": "PC",
    "PROBATION OTHER": "PO",
    "PROBATION REVOKED": "PR",
    "REMANDED TO DISTRICT COURT": "RM",
    DISP_SUPERSEDING_INDICTMENT: "SI",
    "TRANSFERRED TO DISTRICT COURT": "TD",
    "WAIVER - CLERK": "WC",
    "WAIVER - MAGISTRATE": "WM",
    "WAIVER OF EXTRADITION": "WE",
    "WAIVER OF PROBABLE CAUSE": "WP",
}

"""
GTL is not a disposition method that is found in the CIPRS records. It is a "derived" disposition method used on the
expungable summary document
"""
DISP_GUILTY_TO_LESSER = "GTL"

VERDICT_GUILTY = "GUILTY"

GENERATED_PETITION_ADMIN_FIELDS = (
    "id",
    "username",
    "batch_id",
    "form_type",
    "number_of_charges",
    "created",
)
