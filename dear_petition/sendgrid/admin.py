from django.contrib import admin, messages
from django.contrib.postgres.fields import JSONField
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

from .models import Email, Attachment
from .widgets import PrettyJSONWidget


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 0


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}
    readonly_fields = ("attachment_count",)
    list_display = (
        "id",
        "recipient",
        "sender",
        "attachment_count",
        "spam_score",
        "date_created",
        "subject",
    )
    list_filter = ("date_created",)
    date_hierarchy = "date_created"
    search_fields = ("payload", "id")
    ordering = ("-date_created",)
    inlines = (AttachmentInline,)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "content_id",
        "type",
    )
    list_filter = ("type",)
    search_fields = ("name", "email__recipient", "content_id", "id")
    raw_id_fields = ("email",)
