import logging

from dear_petition.petition.models import Batch, CIPRSRecord

from .parse import parse_portal_document

__all__ = ("import_portal_record",)

logger = logging.getLogger(__name__)


def import_portal_record(user, source):
    """Import eCourts Portal records into models."""
    logger.info("Importing Portal record")
    data = parse_portal_document(source)
    batch, _ = Batch.objects.get_or_create(user=user, label=data["Defendant"]["Name"])
    record = CIPRSRecord(batch=batch, data=data)
    record.refresh_record_from_data()
    record.save()
