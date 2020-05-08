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
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CIPRSRecordSerializer,
    ContactSerializer,
    BatchSerializer,
    OffenseSerializer,
    OffenseRecordSerializer,
    GeneratePetitionSerializer,
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


class GeneratePetitionView(viewsets.GenericViewSet):

    serializer_class = GeneratePetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response("OK")
