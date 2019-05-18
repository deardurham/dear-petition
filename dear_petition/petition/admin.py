from django.contrib import admin

from dear_petition.petition import models


@admin.register(models.CIPRSRecord)
class CIPRSRecordAdmin(admin.ModelAdmin):

    list_display = ('pk', 'label', 'report_pdf', 'date_uploaded')
    ordering = ('-date_uploaded',)
