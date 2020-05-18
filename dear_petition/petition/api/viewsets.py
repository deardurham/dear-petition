import json

from django.http import FileResponse

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
from rest_framework import parsers
from .serializers import (
    UserSerializer,
    CIPRSRecordSerializer,
    ContactSerializer,
    BatchSerializer,
    OffenseSerializer,
    OffenseRecordSerializer,
    GeneratePetitionSerializer,
)
from dear_petition.petition.etl import import_ciprs_records
from dear_petition.petition.export import generate_petition_pdf
from rest_framework import status


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
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        files = self.request.data.getlist("files")
        batch = import_ciprs_records(files=files, user=self.request.user)
        return {"id": batch.pk}

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class GeneratePetitionView(viewsets.GenericViewSet):

    serializer_class = GeneratePetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        buffer = generate_petition_pdf(serializer.data["petition"], serializer.data)
        resp = FileResponse(buffer)
        resp["Content-Type"] = "application/pdf"
        resp["Content-Disposition"] = 'inline; filename="petition.pdf"'
        return resp
