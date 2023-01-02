import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from dear_petition.petition import models as pm

logger = logging.getLogger(__name__)


def clean_stale_data():
    now = timezone.now()
    stale_time = now - timedelta(hours=settings.CIPRS_RECORD_LIFETIME_HOURS)
    stale_data = pm.Batch.objects.filter(date_uploaded__lt=stale_time)
    num_deleted, _ = stale_data.delete()
    logger.info(f"Deleted {num_deleted} batches.")
    return num_deleted


@shared_task(soft_time_limit=600, time_limit=630)
def clean_stale_data_task():
    clean_stale_data()
