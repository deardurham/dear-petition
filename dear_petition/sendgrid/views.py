from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import EmailForm


@csrf_exempt
@require_POST
def webhook(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        print(form.errors)
        return HttpResponse(status=500)

    return HttpResponse(status=208)
