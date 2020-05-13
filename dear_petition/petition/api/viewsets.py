from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
)
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import (
    UserSerializer,
    CIPRSRecordSerializer,
    ContactSerializer,
    BatchSerializer,
    OffenseSerializer,
    OffenseRecordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CIPRSRecordViewSet(viewsets.ModelViewSet):

    queryset = CIPRSRecord.objects.all()
    serializer_class = CIPRSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseViewSet(viewsets.ModelViewSet):
    queryset = Offense.objects.all()
    serializer_class = OffenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseRecordViewSet(viewsets.ModelViewSet):
    queryset = OffenseRecord.objects.all()
    serializer_class = OffenseRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class BatchViewSet(viewsets.ModelViewSet):

    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
