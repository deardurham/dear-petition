from email.utils import parseaddr
import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import EmailForm
from .actions import notify_sendgrid_listeners


logger = logging.getLogger(__name__)


def email_is_allowed(addr, allowed_addrs):
    """Return if addr is in allowed_addrs (a list of email addresses or domains)"""
    if not allowed_addrs:
        return True
    _, email = parseaddr(addr)
    _, _, domain = email.rpartition("@")
    return email in allowed_addrs or domain in allowed_addrs


@csrf_exempt
@require_POST
def webhook(request):
    form = EmailForm(request=request)
    if not form.is_valid():
        logger.warning(f"Webhook validation failed: {form.errors.as_json()}")
        return HttpResponse(status=400)
    sender = form.cleaned_data["sender"]
    allowed_senders = getattr(settings, "SENDGRID_ALLOWED_SENDERS", [])
    if email_is_allowed(addr=sender, allowed_addrs=allowed_senders):
        email = form.save()
        notify_sendgrid_listeners(email_id=email.id)
    else:
        logger.warning(f"Email address not allowed {sender}")
    return HttpResponse(status=201)
