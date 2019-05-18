import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import CIPRSRecord
from .forms import UploadFileForm


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
    context = {
        'record': record,
        'data_pretty': json.dumps(record.data, sort_keys=True, indent=4)
    }
    return render(request, 'petition/view.html', context)
