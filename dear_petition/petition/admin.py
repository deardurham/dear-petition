from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect

from dear_petition.petition import models


@admin.register(models.CIPRSRecord)
class CIPRSRecordAdmin(admin.ModelAdmin):

    actions = ('action_parse_report_pdf',)
    list_display = ('pk', 'label', 'report_pdf', 'date_uploaded')
    ordering = ('-date_uploaded',)

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
        if 'error' in report.data:
            messages.error(request, "An error occurred")
        else:
            messages.success(request, "Parsed successfully")
        return redirect('admin:petition_ciprsrecord_changelist')
    action_parse_report_pdf.short_description = 'Parse PDF Report...'


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'category', 'address1')
    list_filter = ('category',)
    ordering = ('category', 'name')
