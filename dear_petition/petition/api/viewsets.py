from dear_petition.users.models import User
from dear_petition.petition.models import CIPRSRecord, Contact, Batch
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import (
    UserSerializer,
    CIPRSRecordSerializer,
    ContactSerializer,
    BatchSerializer,
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CIPRSRecordViewSet(viewsets.ModelViewSet):

    queryset = CIPRSRecord.objects.all()
    serializer_class = CIPRSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class BatchViewSet(viewsets.ModelViewSet):

    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
