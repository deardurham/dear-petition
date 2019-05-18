from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm


def upload_report(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'petition/upload.html', {'form': form})
