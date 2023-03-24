import logging
from django.urls import reverse
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
    Petition,
    PetitionDocument,
)
from dear_petition.petition.constants import ATTACHMENT, DISMISSED


logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    admin_url = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(source="is_staff", default=False)

    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "email",
            "is_admin",
            "is_staff",
            "admin_url",
            "last_login",
        ]
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
        ciprs_record = offense_record.offense.ciprs_record
        try:
            return ciprs_record.offense_date.date()
        except AttributeError:
            logger.warning(f"{ciprs_record} missing offense date")
            return None

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
    formatted_address = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    def get_formatted_address(self, contact_obj):
        lines = [contact_obj.address1]
        if contact_obj.address2:
            lines.append(contact_obj.address2)
        return ", ".join(lines)

    class Meta:
        model = Contact
        fields = [
            "pk",
            "name",
            "category",
            "address1",
            "address2",
            "formatted_address",
            "city",
            "state",
            "zipcode",
            "user",
        ]

class ClientSerializer(ContactSerializer):
    address1 = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    zipcode = serializers.CharField(required=True)

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
            "agencies",
            "documents",
        ]


class PetitionDocumentSerializer(serializers.ModelSerializer):
    form_type = serializers.CharField()
    county = serializers.CharField()
    jurisdiction = serializers.CharField()

    class Meta:
        model = PetitionDocument
        fields = [
            "pk",
            "form_type",
            "county",
            "jurisdiction",
            "offense_records",
        ]


class ParentPetitionSerializer(PetitionSerializer):
    base_document = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    offense_records = serializers.SerializerMethodField()
    active_records = serializers.SerializerMethodField()
    agencies = ContactSerializer(many=True, read_only=True)

    class Meta(PetitionSerializer.Meta):
        fields = PetitionSerializer.Meta.fields + [
            "base_document",
            "attachments",
            "active_records",
        ]

    def get_base_document(self, instance):
        return PetitionDocumentSerializer(
            PetitionDocument.objects.get(
                petition_id=instance.id, previous_document__isnull=True
            )
        ).data

    def get_attachments(self, instance):
        return PetitionDocumentSerializer(
            PetitionDocument.objects.filter(
                petition_id=instance.id, previous_document__isnull=False
            ).order_by("pk"),
            many=True,
        ).data

    def get_offense_records(self, petition):
        offense_records = petition.offense_records.all()
        return OffenseRecordSerializer(offense_records, many=True).data

    def get_active_records(self, petition):
        return petition.offense_records.filter(
            petitionoffenserecord__active=True
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
            "automatic_delete_date",
        ]
        read_only_fields = ["user", "automatic_delete_date"]


class BatchDetailSerializer(serializers.ModelSerializer):
    records = CIPRSRecordSerializer(many=True, read_only=True)
    petitions = serializers.SerializerMethodField()
    attorney_id = serializers.PrimaryKeyRelatedField(
        source='attorney', queryset=Contact.objects.filter(category='attorney'), write_only=True, required=False
    )
    attorney = ContactSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        source='client', queryset=Contact.objects.filter(category='client'), write_only=True, required=False
    )
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Batch
        fields = [
            "pk",
            "label",
            "date_uploaded",
            "user",
            "records",
            "petitions",
            "attorney",
            "attorney_id",
            "client",
            "client_id",
        ]
        read_only_fields = ["user", "pk", "date_uploaded", "records", "petitions"]

    def get_petitions(self, instance):
        """Return sorted and structured petitions with associated attachments"""
        parent_petitions = Petition.objects.filter(
            batch=instance.pk,
        ).order_by("county", "jurisdiction")
        return ParentPetitionSerializer(parent_petitions, many=True).data


class MyInboxSerializer(serializers.ModelSerializer):
    total_files = serializers.IntegerField()
    total_emails = serializers.IntegerField()
    total_petitions = serializers.SerializerMethodField()
    total_ciprs_records = serializers.SerializerMethodField()
    automatic_delete_date = serializers.DateTimeField()

    class Meta:
        model = Batch
        fields = [
            "pk",
            "label",
            "date_uploaded",
            "automatic_delete_date",
            "total_files",
            "total_emails",
            "total_petitions",
            "total_ciprs_records",
        ]

    def get_total_petitions(self, instance):
        # workaround for multiple table annotation failure: https://code.djangoproject.com/ticket/10060
        return instance.petitions.count()

    def get_total_ciprs_records(self, instance):
        # workaround for multiple table annotation failure: https://code.djangoproject.com/ticket/10060
        return instance.records.count()


class GeneratePetitionSerializer(serializers.Serializer):

    documents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PetitionDocument.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_documents(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                "Must select at least one document for pdf generation"
            )
        return value


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
