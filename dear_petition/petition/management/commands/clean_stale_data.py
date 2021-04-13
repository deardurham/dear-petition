import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from dear_petition.petition import models as pm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    https://github.com/deardurham/dear-petition/issues/206
    Need to delete data 48 hours after petition is generated to protect the privacy of the clients.
    """

    def handle(self, *args, **options):
        now = timezone.now()
        stale_time = now - timedelta(hours=48)
        stale_data = pm.Batch.objects.filter(
            petitions__created__gt=stale_time
        ).distinct()
        num_deleted, _ = stale_data.delete()
        logger.info(f"Deleted {num_deleted} batches.")
