
DISTRICT_COURT = "D"
SUPERIOR_COURT = "S"
NOT_AVAILABLE = "N/A"

JURISDICTION_CHOICES = (
    (DISTRICT_COURT, "DISTRICT COURT"),
    (SUPERIOR_COURT, "SUPERIOR COURT"),
    (NOT_AVAILABLE, "NOT AVAILABLE"),
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

