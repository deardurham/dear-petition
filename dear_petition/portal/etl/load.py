import logging

from dear_petition.petition.models import Batch, CIPRSRecord
from dear_petition.petition.etl.load import create_batch_petitions

from .transform import transform_portal_record

__all__ = ("import_portal_record",)

logger = logging.getLogger(__name__)


def import_portal_record(user, source: str, location: str):
    """Import eCourts Portal records into models."""
    logger.info("Importing Portal record")
    data = transform_portal_record(source, location)
    batch, _ = Batch.objects.get_or_create(user=user, label=data["Defendant"]["Name"])
    record = CIPRSRecord(batch=batch, data=data)
    record.refresh_record_from_data()
    record.save()
    create_batch_petitions(batch)
