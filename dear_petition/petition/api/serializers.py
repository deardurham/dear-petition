from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
)
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class OffenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenseRecord
        fields = ["offense", "law", "code", "action", "severity", "description"]


class OffenseSerializer(serializers.ModelSerializer):
    offense_records = OffenseRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Offense
        fields = [
            "ciprs_record",
            "disposed_on",
            "disposition_method",
            "offense_records",
        ]


class CIPRSRecordSerializer(serializers.ModelSerializer):
    offenses = OffenseSerializer(many=True, read_only=True)

    class Meta:
        model = CIPRSRecord
        fields = ["batch", "date_uploaded", "label", "offenses"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "name",
            "category",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        ]


class BatchSerializer(serializers.ModelSerializer):
    ciprsrecords = CIPRSRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ["label", "date_uploaded", "user", "ciprsrecords"]
