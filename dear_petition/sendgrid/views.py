import logging

from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import EmailForm
from .actions import link_email_to_user


logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def webhook(request):
    form = EmailForm(request=request)
    if not form.is_valid():
        logger.warning(f"Webhook validation failed: {form.errors.as_json()}")
        return HttpResponse(status=400)
    email = form.save()
    link_email_to_user(email_id=email.id)
    return HttpResponse(status=201)
