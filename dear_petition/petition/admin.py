from django.contrib import admin, messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

from dear_petition.petition import models


@admin.register(models.CIPRSRecord)
class CIPRSRecordAdmin(admin.ModelAdmin):

    actions = ("action_parse_report_pdf",)
    list_display = ("pk", "label", "batch", "date_uploaded")
    list_filter = ("date_uploaded",)
    date_hierarchy = "date_uploaded"
    search_fields = ("label",)
    ordering = ("-date_uploaded",)

    def action_parse_report_pdf(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        if len(selected) > 1:
            msg = "This action currently only supports a single report"
            messages.error(request, msg)
            return
        pk = selected[0]
        report = get_object_or_404(models.CIPRSRecord, pk=pk)
        report.data = report.parse_report()
        report.save()
        if "error" in report.data:
            messages.error(request, "An error occurred")
        else:
            messages.success(request, "Parsed successfully")
        return redirect("admin:petition_ciprsrecord_changelist")

    action_parse_report_pdf.short_description = "Parse PDF Report..."


class CIPRSRecordInline(admin.StackedInline):
    model = models.CIPRSRecord
    extra = 1


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("pk", "label", "record_count", "user", "date_uploaded")
    list_filter = ("date_uploaded", "user")
    date_hierarchy = "date_uploaded"
    search_fields = ("label",)
    ordering = ("-date_uploaded", "label")
    inlines = (CIPRSRecordInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_record_count=Count("records", distinct=True),)
        return queryset

    def record_count(self, obj):
        return obj._record_count


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ("pk", "name", "category", "address1")
    list_filter = ("category",)
    ordering = ("category", "name")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("pk", "user", "batch", "time")
    search_fields = ("batch__label",)
    date_hierarchy = "time"
    list_filter = ("user", "time")
    ordering = ("-time",)
