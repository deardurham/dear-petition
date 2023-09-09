import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import BookmarkletDataForm
from .load import import_portal_record


logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def bookmarklet_handler(request):
    form = BookmarkletDataForm(request.POST)
    if not form.is_valid():
        logger.warning(f"Bookmarklet validation failed: {form.errors.as_json()}")
        return HttpResponse(status=400)

    import_portal_record(
        user=form.cleaned_data["user"], source=form.cleaned_data["source"]
    )
    return HttpResponse(status=201)
