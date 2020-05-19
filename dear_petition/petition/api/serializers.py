from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
    Petition,
)
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "email"]


class OffenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenseRecord
        fields = ["pk", "offense", "law", "code", "action", "severity", "description"]


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
    class Meta:
        model = Petition
        fields = ["pk", "form_type", "county", "jurisdiction"]


class BatchSerializer(serializers.ModelSerializer):
    records = CIPRSRecordSerializer(many=True, read_only=True)
    petitions = PetitionSerializer(many=True, read_only=True)

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


class GeneratePetitionSerializer(serializers.Serializer):

    petition = serializers.ChoiceField(
        choices=[], style={"base_template": "input.html"},
    )
    ssn = serializers.CharField(label="SSN")
    drivers_license = serializers.CharField(label="Driver's License #")
    attorney = serializers.ChoiceField(
        choices=Contact.objects.filter(category="attorney").values_list("pk", "name")
    )
    agencies = serializers.MultipleChoiceField(
        choices=Contact.objects.filter(category="agency").values_list("pk", "name")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["petition"].choices = Petition.objects.values_list("pk", "pk")

    def validate_petition(self, value):
        return Petition.objects.get(pk=value)

    def validate_attorney(self, value):
        return Contact.objects.get(pk=value)

    def validate_agencies(self, value):
        return Contact.objects.filter(pk__in=value)
