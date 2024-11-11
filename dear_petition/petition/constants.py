from model_utils import Choices

PARSER_MODE = 2

DISTRICT_COURT = "D"
SUPERIOR_COURT = "S"
NOT_AVAILABLE = "N/A"

JURISDICTION_MAP = {
    DISTRICT_COURT: "DISTRICT COURT",
    SUPERIOR_COURT: "SUPERIOR COURT",
    NOT_AVAILABLE: "NOT AVAILABLE",
}

JURISDICTION_CHOICES = Choices(*[(k, v) for k, v in JURISDICTION_MAP.items()])

OFFENSE_HEADERS = Choices(
    (DISTRICT_COURT, "District Court Offense Information"),
    (SUPERIOR_COURT, "Superior Court Offense Information"),
)

MALE = "M"
FEMALE = "F"
UNKNOWN = "U"

SEX_MAP = {"Male": MALE, "Female": FEMALE, "Unknown": UNKNOWN, "NOT AVAILABLE": NOT_AVAILABLE}

SEX_CHOICES = Choices(*[(v, k) for k, v in SEX_MAP.items()])

CONTACT_CATEGORIES = Choices(("agency", "Agency"), ("attorney", "Attorney"), ("client", "Client"))

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

CHARGED = "CHARGED"
CONVICTED = "CONVICTED"
ARRAIGNED = "ARRAIGNED"
GUILTY = "GUILTY"

ACTIONS = Choices(
    (CHARGED, CHARGED),
    (CONVICTED, CONVICTED),
    (ARRAIGNED, ARRAIGNED),
    (GUILTY, GUILTY),
)

COMMENT_MAX_LENGTH = 8192

NEW_COMMENT_EMAIL_SUBJECT = "New comment available for batch #{batch}"
NEW_COMMENT_EMAIL_MESSAGE = (
    "There is a new comment available for batch#{batch}.{user}\n\n\n{text}\n\nSee it here:{link}"
)

DATA_PETITION = "DATA-PETITION"

MISDEMEANOR = "AOC-CR-281"
ATTACHMENT = "AOC-CR-285"
DISMISSED = "AOC-CR-287"
NOT_GUILTY = "AOC-CR-288"
UNDERAGED_CONVICTIONS = "AOC-CR-293"
ADULT_FELONIES = "AOC-CR-297"
ADULT_MISDEMEANORS = "AOC-CR-298"
ADDENDUM_3B = "Addendum 3B"

PETITION_FORM_TYPES = Choices(
    (MISDEMEANOR, MISDEMEANOR),
    (ATTACHMENT, ATTACHMENT),
    (DISMISSED, DISMISSED),
    (NOT_GUILTY, NOT_GUILTY),
    (UNDERAGED_CONVICTIONS, UNDERAGED_CONVICTIONS),
    (ADULT_FELONIES, ADULT_FELONIES),
    (ADULT_MISDEMEANORS, ADULT_MISDEMEANORS),
)
ADDENDUM_FORM_TYPES = Choices(
    (ADDENDUM_3B, ADDENDUM_3B),
)
FORM_TYPES = PETITION_FORM_TYPES + ADDENDUM_FORM_TYPES
INACTIVE_BY_DEFAULT_FORM_TYPES = (
    UNDERAGED_CONVICTIONS,
    ADULT_FELONIES,
    ADULT_MISDEMEANORS,
)
STATUTES = {
    DISMISSED: "146(a)",
    NOT_GUILTY: "146(a2)",
    UNDERAGED_CONVICTIONS: "145.8A",
    ADULT_FELONIES: "145.5F",
    ADULT_MISDEMEANORS: "145.5M",
}

SEVERITIES = Choices(
    ("TRAFFIC", "Traffic"),
    ("INFRACTION", "Infraction"),
    ("FELONY", "Felony"),
    ("MISDEMEANOR", "Misdemeanor"),
)

NORTH_CAROLINA = "NC"
DURHAM_COUNTY = "DURHAM"

DISTRICT_COURT_WITHOUT_DA_LEAVE = "Dismissal without Leave by DA"

CIPRS_DISPOSITION_METHODS_DISMISSED = (
    DISTRICT_COURT_WITHOUT_DA_LEAVE,
    "Dismissed by Court",
    "Deferred Prosecution Dismissal",
    "Discharge and Dismissal",
    "Conditional Discharge",
    "No Probable Cause",
    "Never To Be Served",
    "Deferred Proceeding or Deferred Prosecution Dismissal",
)

PORTAL_DISPOSITION_METHODS_DISMISSED = (
    "District Dismissed by the Court - No Plea Agreement",
    "District Dismissed by the Court - Plea Agreement",
    "Superior Dismissed by the Court - No Plea Agreement",
    "Superior Dismissed by the Court - Plea Agreement",
    "District Dismissed by Court - Speedy Trial",
    "Superior Dismissed by Court - Speedy Trial",
    "VD-District Dismissals w/o Leave by DA - No Plea Agreement",
    "VD-District Dismissals w/o Leave by DA - Per Plea Agreement",
    "VD-Superior Dismissals w/o Leave by DA - No Plea Agreement",
    "VD-Superior Dismissals w/o Leave by DA - Per Plea Agreement",
    "District Not Guilty - Judge",
    "Not Guilty - Jury",
    "Not Guilty - Magistrate",
    "Superior Not Guilty - Judge",
    "District Not Responsible - Judge",
    "Not Responsible - Jury",
    "Superior Not Responsible - Judge",
    "District Dismissed Incapacity without Leave - No Plea Agreement",
    "District Dismissed Incapacity without Leave - Plea Agreement",
    "Superior Dismissed Incapacity without Leave - No Plea Agreement",
    "Superior Dismissed Incapacity without Leave - Plea Agreement",
    "No Probable Cause Found",
    "District Deferred Proceeding/Prosecution Dismissal",
    "Superior Deferred Proceeding/Prosecution Dismissal",
    "District Never to Be Served",
)

PORTAL_DISPOSITION_METHODS_NOT_GUILTY = (
    "District Not Guilty - Judge",
    "Superior Not Guilty - Judge",
    "Not Guilty - Jury",
)

PORTAL_DISPOSITION_METHODS_CONVICTED = (
    "District Guilty - Judge",
    "Superior Guilty - Judge",
    "Guilty - Jury",
)

DISP_METHOD_SUPERSEDING_INDICTMENT = "SUPERSEDING INDICTMENT OR PROCESS"
DISP_METHOD_WAIVER_OF_PROBABLE_CAUSE = "WAIVER OF PROBABLE CAUSE"


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
    "DISPOSED BY JUDGE": "JU",
    "FIGHT EXTRADITION": "FE",
    "HABEAS CORPUS HEARING": "HC",
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
    DISP_METHOD_SUPERSEDING_INDICTMENT: "SI",
    "TRANSFERRED TO DISTRICT COURT": "TD",
    "WAIVER - CLERK": "WC",
    "WAIVER - MAGISTRATE": "WM",
    "WAIVER OF EXTRADITION": "WE",
    DISP_METHOD_WAIVER_OF_PROBABLE_CAUSE: "WP",
}

VERDICT_GUILTY = "GUILTY"
VERDICT_NOT_GUILTY = "NOT GUILTY"
VERDICT_GUILTY_TO_LESSER = "GUILTY TO LESSER"
VERDICT_PRAYER_FOR_JUDGMENT = "PRAYER FOR JUDGMENT"
VERDICT_RESPONSIBLE = "RESPONSIBLE"
VERDICT_RESPONSIBLE_TO_LESSER = "RESPONSIBLE TO LESSER"

VERDICT_CODE_GUILTY = "GU"
VERDICT_CODE_GUILTY_TO_LESSER = "GL"
VERDICT_CODE_PRAYER_FOR_JUDGMENT = "PJC"
VERDICT_CODE_RESPONSIBLE = "RS"
VERDICT_CODE_RESPONSIBLE_TO_LESSER = "RL"

VERDICT_CODE_MAP = {
    VERDICT_GUILTY: VERDICT_CODE_GUILTY,
    VERDICT_GUILTY_TO_LESSER: VERDICT_CODE_GUILTY_TO_LESSER,
    "JUDGMENT ARRESTED": "JA",
    VERDICT_NOT_GUILTY: "NG",
    "NOT RESPONSIBLE": "NR",
    VERDICT_PRAYER_FOR_JUDGMENT: VERDICT_CODE_PRAYER_FOR_JUDGMENT,
    VERDICT_RESPONSIBLE: VERDICT_CODE_RESPONSIBLE,
    VERDICT_RESPONSIBLE_TO_LESSER: VERDICT_CODE_RESPONSIBLE_TO_LESSER,
}

GENERATED_PETITION_ADMIN_FIELDS = (
    "id",
    "username",
    "batch_id",
    "form_type",
    "number_of_charges",
    "created",
)

SEVERITY_FELONY = "FELONY"
SEVERITY_MISDEMEANOR = "MISDEMEANOR"
CHARGED_DEGREE_FELONY = ("FA", "FB", "FC", "FD", "FE", "FF", "FG", "FH", "FI", "FNC")
CHARGED_DEGREE_MISDEMEANOR = ("MA1", "M1", "M2", "M3", "MNC")
