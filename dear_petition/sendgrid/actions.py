import logging

from dear_petition.users.models import User
from dear_petition.petition.etl.load import import_ciprs_records

from .models import Email


logger = logging.getLogger(__name__)


def extract_username_and_label(addr):
    """
    Extracts email into parts for importing.

    For example:
        first.last+mylabel@example.com -> first.last, mylabel
    """
    email_username = addr.split("@")[0]
    username_parts = email_username.split("+")
    username = username_parts[0]
    try:
        label = username_parts[1]
    except IndexError:
        label = ""
    return username, label


def link_email_to_user(email_id):
    """
    Associate email attachments to a user and pass off to the ETL process.
    """
    email = Email.objects.get(id=email_id)
    username, label = extract_username_and_label(email.recipient)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        logger.error(f"Username {username} not found for email '{email}'")
        return
    attachment_files = []
    for attachment in email.attachments.all():
        attachment_files.append(attachment.file)
    import_ciprs_records(
        files=attachment_files, user=user, parser_mode=1, batch_label=label
    )
