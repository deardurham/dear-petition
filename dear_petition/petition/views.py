import json
import tempfile

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import CIPRSRecord
from .forms import GeneratePetitionForm, UploadFileForm


@login_required
def upload_report(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save()
            return redirect("view-record", pk=record.pk)
    else:
        form = UploadFileForm()
    return render(request, 'petition/upload.html', {'form': form})


@login_required
def view_record(request, pk):
    record = get_object_or_404(CIPRSRecord, pk=pk)
    if request.method == 'POST':
        form = GeneratePetitionForm(request.POST, record=record)
        if form.is_valid():
            output = form.save()
            return FileResponse(output, filename='petition.pdf', as_attachment=True)
    context = {
        'record': record,
        'data_pretty': json.dumps(record.data, sort_keys=True, indent=4)
    }
    return render(request, 'petition/view.html', context)
