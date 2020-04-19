from dear_petition.users.models import User
from dear_petition.petition.models import CIPRSRecord, Contact, Batch
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class CIPRSRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIPRSRecord
        fields = ["batch", "date_uploaded", "label"]


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
    class Meta:
        model = Batch
        fields = ["label", "date_uploaded", "user"]
