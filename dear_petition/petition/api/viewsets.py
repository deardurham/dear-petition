from dear_petition.users.models import User
from dear_petition.petition.models import (
    CIPRSRecord,
    Contact,
    Batch,
    Offense,
    OffenseRecord,
)
from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import (
    UserSerializer,
    CIPRSRecordSerializer,
    ContactSerializer,
    BatchSerializer,
    OffenseSerializer,
    OffenseRecordSerializer,
    PetitionSerializer,
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

    queryset = Batch.objects.prefetch_related(
        "petitions", "records__offenses__offense_records"
    )
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "put"]


class GeneratePetitionView(viewsets.ViewSet):

    serializer_class = PetitionSerializer

    def create(self, request):
        pass
