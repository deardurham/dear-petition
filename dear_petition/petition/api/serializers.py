from django.urls import reverse

from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
    Petition,
)
from dear_petition.petition.constants import ATTACHMENT, DISMISSED
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from localflavor.us import us_states


class UserSerializer(serializers.HyperlinkedModelSerializer):
    admin_url = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(source="is_staff", default=False)

    class Meta:
        model = User
        fields = ["pk", "username", "email", "is_admin", "is_staff", "admin_url", "last_login"]
        extra_kwargs = {"email": {"required": True, "allow_blank": False}}

    def get_admin_url(self, user_obj):
        url = ""
        if user_obj and user_obj.is_staff:
            url = reverse("admin:index")
        return url

    def create(self, validated_data):
        random_pw = User.objects.make_random_password()
        is_admin = validated_data.get("is_staff", False)
        return User.objects.create_user(
            password=random_pw, is_superuser=is_admin, **validated_data
        )


class OffenseRecordSerializer(serializers.ModelSerializer):
    offense_date = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    disposition_method = serializers.SerializerMethodField()
    file_no = serializers.SerializerMethodField()

    def get_offense_date(self, offense_record):
        return offense_record.offense.ciprs_record.offense_date.date()

    def get_dob(self, offense_record):
        return offense_record.offense.ciprs_record.dob

    def get_disposition_method(self, offense_record):
        return offense_record.offense.disposition_method

    def get_file_no(self, offense_record):
        return offense_record.offense.ciprs_record.file_no

    class Meta:
        model = OffenseRecord
        fields = [
            "pk",
            "offense",
            "law",
            "code",
            "action",
            "severity",
            "description",
            "active",
            "offense_date",
            "dob",
            "disposition_method",
            "file_no",
        ]


class OffenseSerializer(serializers.ModelSerializer):
    offense_records = OffenseRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Offense
        fields = [
            "pk",
            "ciprs_record",
            "disposed_on",
            "disposition_method",
            "offense_records",
            "plea",
            "verdict",
        ]


class CIPRSRecordSerializer(serializers.ModelSerializer):
    offenses = OffenseSerializer(many=True, read_only=True)

    class Meta:
        model = CIPRSRecord
        fields = ["pk", "batch", "date_uploaded", "label", "offenses"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "pk",
            "name",
            "category",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        ]


class PetitionSerializer(serializers.ModelSerializer):
    jurisdiction = serializers.CharField(source="get_jurisdiction_display")

    class Meta:
        model = Petition
        fields = [
            "pk",
            "form_type",
            "county",
            "jurisdiction",
            "offense_records",
        ]


class ParentPetitionSerializer(PetitionSerializer):
    attachments = serializers.SerializerMethodField()
    offense_records = serializers.SerializerMethodField()
    active_records = serializers.SerializerMethodField()

    class Meta(PetitionSerializer.Meta):
        fields = PetitionSerializer.Meta.fields + ["attachments", "active_records"]

    def get_attachments(self, instance):
        return PetitionSerializer(
            instance.attachments.all().order_by("pk"), many=True
        ).data

    def get_offense_records(self, petition):
        offense_records = petition.get_all_offense_records(
            filter_active=False, include_annotations=False
        )
        return OffenseRecordSerializer(offense_records, many=True).data

    def get_active_records(self, petition):
        return petition.get_all_offense_records(
            filter_active=True, include_annotations=False
        ).values_list("id", flat=True)


class BatchSerializer(serializers.ModelSerializer):
    records = CIPRSRecordSerializer(many=True, read_only=True)
    petitions = PetitionSerializer(many=True, read_only=True)
    parser_mode = serializers.IntegerField(default=1)

    class Meta:
        model = Batch
        fields = [
            "pk",
            "label",
            "date_uploaded",
            "user",
            "records",
            "petitions",
            "parser_mode",
        ]
        read_only_fields = ["user"]


class BatchDetailSerializer(serializers.ModelSerializer):
    records = CIPRSRecordSerializer(many=True, read_only=True)
    petitions = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = [
            "pk",
            "label",
            "date_uploaded",
            "user",
            "records",
            "petitions",
        ]
        read_only_fields = ["user"]

    def get_petitions(self, instance):
        """Return sorted and structured petitions with associated attachments"""
        parent_petitions = Petition.objects.filter(
            batch=instance.pk, parent__isnull=True
        ).order_by("county", "jurisdiction")
        return ParentPetitionSerializer(parent_petitions, many=True).data


class GeneratePetitionSerializer(serializers.Serializer):

    petition = serializers.ChoiceField(
        choices=[],
        style={"base_template": "input.html"},
    )
    name_petitioner = serializers.CharField(label="Petitioner Name")
    address1 = serializers.CharField(label="Address Line 1")
    address2 = serializers.CharField(
        label="Address Line 2", required=False, allow_blank=True
    )
    city = serializers.CharField(label="City")
    state = serializers.ChoiceField(choices=us_states.US_STATES)
    zip_code = serializers.CharField(label="Zip Code")
    attorney = serializers.ChoiceField(choices=[])
    agencies = serializers.MultipleChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["petition"].choices = Petition.objects.values_list("pk", "pk")
        self.fields["attorney"].choices = Contact.objects.filter(
            category="attorney"
        ).values_list("pk", "name")
        self.fields["agencies"].choices = Contact.objects.filter(
            category="agency"
        ).values_list("pk", "name")

    def validate_petition(self, value):
        return Petition.objects.get(pk=value)

    def validate_attorney(self, value):
        return Contact.objects.get(pk=value)

    def validate_agencies(self, value):
        return Contact.objects.filter(pk__in=value)


class TokenObtainPairCookieSerializer(TokenObtainPairSerializer):
    """
    Subclass TokenObtainPairSerializer from simplejwt so that we can add the requesting user
    to response body
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user_serializer = UserSerializer(self.user)
        data["user"] = user_serializer.data
        return data


class DataPetitionSerializer(serializers.Serializer):

    form_type = serializers.ChoiceField(
        choices=((DISMISSED, DISMISSED), (ATTACHMENT, ATTACHMENT)), initial=DISMISSED
    )
    form_context = serializers.JSONField()
