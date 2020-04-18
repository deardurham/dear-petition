from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import CIPRSRecord, Batch, Comment
from .forms import GeneratePetitionForm, UploadFileForm, CommentForm
from .permissions import is_owner


@transaction.atomic
@login_required
def upload_report(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            batch = form.save(user=request.user)
            return redirect("create-petition", pk=batch.pk)
    else:
        form = UploadFileForm()
    return render(request, "petition/upload.html", {"form": form})


@login_required
def view_record(request, pk):
    record = get_object_or_404(CIPRSRecord, pk=pk)
    if not is_owner(request.user, record.batch):
        raise PermissionDenied
    if "_meta" in record.data and "source" in record.data["_meta"]:
        source = record.data["_meta"]["source"]
    else:
        source = ""
    context = {"record": record, "source": source}
    return render(request, "petition/view.html", context)


@login_required
def create_petition(request, pk, tab="petition"):
    batch = get_object_or_404(Batch, pk=pk)
    if not is_owner(request.user, batch) and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == "POST":
        form = GeneratePetitionForm(request.POST, batch=batch)
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
        form = GeneratePetitionForm(batch=batch)
    context = {
        "form": form,
        "batch": batch,
        "tab": tab,
        "comment_form": CommentForm(auto_id=False),
    }
    return render(request, "petition/create.html", context)


@login_required
@require_POST
def create_comment(request, batch_id):
    batch = get_object_or_404(Batch, pk=batch_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.batch = batch
        instance.save()
        return redirect("create-petition", pk=batch.pk, tab="comments")
