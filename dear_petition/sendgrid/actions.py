import functools
import logging

from django.conf import settings
from django.utils.module_loading import import_string


logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=None)
def get_listener(import_path):
    """Import a dotted module path and return the function instance"""
    return import_string(import_path)


def get_listeners():
    """Return list of imported settings.SENDGRID_WEBHOOK_LISTENERS"""
    for listener_path in getattr(settings, "SENDGRID_WEBHOOK_LISTENERS", []):
        yield get_listener(listener_path)


def notify_sendgrid_listeners(email_id):
    """Call all SENDGRID_WEBHOOK_LISTENERS with email_id."""
    for listener in get_listeners():
        listener(email_id=email_id)
