from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import CIPRSRecord
from .forms import GeneratePetitionForm, UploadFileForm


@login_required
def upload_report(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save()
            return redirect("view-record", pk=record.pk)
    else:
        form = UploadFileForm()
    return render(request, "petition/upload.html", {"form": form})


@login_required
def view_record(request, pk):
    record = get_object_or_404(CIPRSRecord, pk=pk)
    if request.method == "POST":
        form = GeneratePetitionForm(request.POST, record=record)
        if form.is_valid():
            output = form.save()
            resp = FileResponse(output)
            resp["Content-Type"] = "application/pdf"
            if form.cleaned_data["as_attachment"]:
                resp["Content-Disposition"] = 'attachment; filename="petition.pdf"'
            else:
                resp["Content-Disposition"] = 'inline; filename="petition.pdf"'
            return resp
    else:
        form = GeneratePetitionForm(record=record)
    if "_meta" in record.data and "source" in record.data["_meta"]:
        source = record.data["_meta"]["source"]
    else:
        source = ""
    context = {"form": form, "record": record, "source": source}
    return render(request, "petition/view.html", context)
