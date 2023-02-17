from django.contrib import admin, messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

from dear_petition.petition import models
from dear_petition.petition import constants


@admin.register(models.CIPRSRecord)
class CIPRSRecordAdmin(admin.ModelAdmin):

    list_display = (
        "pk",
        "label",
        "file_no",
        "jurisdiction",
        "county",
        "sex",
        "race",
        "case_status",
        "date_uploaded",
    )
    list_filter = (
        "date_uploaded",
        "jurisdiction",
        "county",
        "sex",
        "race",
        "case_status",
    )
    date_hierarchy = "date_uploaded"
    search_fields = ("label", "batch__label", "file_no")
    ordering = ("-date_uploaded",)
    raw_id_fields = ("batch", "batch_file")


class CIPRSRecordInline(admin.StackedInline):
    model = models.CIPRSRecord
    extra = 1
    raw_id_fields = ("batch_file",)


class OffenseRecordInline(admin.StackedInline):
    model = models.OffenseRecord
    extra = 1


@admin.register(models.Offense)
class OffenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "batch",
        "file_no",
        "disposed_on",
        "disposition_method",
        "offense_record_count",
    )
    list_filter = ("disposed_on", "disposition_method")
    date_hierarchy = "disposed_on"
    ordering = (
        "-ciprs_record__batch",
        "ciprs_record__file_no",
        "id",
    )
    inlines = (OffenseRecordInline,)
    raw_id_fields = ("ciprs_record",)
    list_select_related = ("ciprs_record__batch",)
    search_fields = ("ciprs_record__file_no", "ciprs_record__batch__label")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _offense_record_count=Count("offense_records", distinct=True),
        )
        return queryset

    def offense_record_count(self, obj):
        return obj._offense_record_count

    @admin.display(ordering="ciprs_record__batch")
    def batch(self, obj):
        return obj.ciprs_record.batch

    @admin.display(ordering="ciprs_record__file_no", description="CIPRS File No")
    def file_no(self, obj):
        return obj.ciprs_record.file_no


@admin.register(models.OffenseRecord)
class OffenseRecordAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "batch",
        "offense",
        "law",
        "action",
        "severity",
        "description",
    )
    list_filter = (
        "law",
        "code",
        "severity",
    )
    search_fields = (
        "description",
        "law",
        "code",
        "offense__ciprs_record__file_no",
    )
    ordering = (
        "-offense__ciprs_record__batch",
        "offense__ciprs_record__file_no",
        "offense",
    )
    raw_id_fields = ("offense",)

    @admin.display(ordering="offense__ciprs_record__batch")
    def batch(self, obj):
        return obj.offense.ciprs_record.batch


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("pk", "label", "record_count", "user", "date_uploaded")
    list_filter = ("date_uploaded", "user")
    date_hierarchy = "date_uploaded"
    search_fields = ("label",)
    ordering = ("-date_uploaded", "label")
    raw_id_fields = ("emails",)
    inlines = (CIPRSRecordInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _record_count=Count("records", distinct=True),
        )
        return queryset

    def record_count(self, obj):
        return obj._record_count


@admin.register(models.BatchFile)
class BatchFileAdmin(admin.ModelAdmin):
    list_display = ("pk", "file", "batch", "date_uploaded")
    list_filter = ("date_uploaded",)
    date_hierarchy = "date_uploaded"
    search_fields = (
        "file",
        "batch__label",
    )
    raw_id_fields = ("batch",)
    ordering = ("-date_uploaded",)


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


@admin.register(models.Petition)
class PetitionAdmin(admin.ModelAdmin):

    list_display = ("pk", "batch", "form_type", "county", "jurisdiction")
    search_fields = ("batch__label",)
    list_filter = ("form_type", "county", "jurisdiction")
    ordering = ("-batch__date_uploaded",)
    raw_id_fields = ("batch", "offense_records")


@admin.register(models.PetitionDocument)
class PetitionDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "batch",
        "petition",
        "is_an_attachment",
        "offense_record_count",
    )
    ordering = ("-petition__batch", "id")
    raw_id_fields = ("petition", "offense_records", "previous_document")
    list_select_related = (
        "petition__batch",
        "previous_document__petition",
    )
    search_fields = ("petition__batch__label",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _offense_record_count=Count("offense_records", distinct=True)
        )
        return queryset

    def offense_record_count(self, obj):
        return obj._offense_record_count

    @admin.display(ordering="petition__batch")
    def batch(self, obj):
        return obj.petition.batch

    @admin.display(boolean=True, description="Is attachment?")
    def is_an_attachment(self, obj):
        return obj.is_attachment


@admin.register(models.GeneratedPetition)
class GeneratedPetitionAdmin(admin.ModelAdmin):

    date_hierarchy = "created"
    list_display = constants.GENERATED_PETITION_ADMIN_FIELDS
    list_filter = ("form_type", "created", "username")
    ordering = ("-created",)
    readonly_fields = (
        "username",
        "batch_id",
        "form_type",
        "number_of_charges",
        "county",
        "jurisdiction",
        "race",
        "sex",
        "age",
    )
    search_fields = ("username", "batch_id", "id")
