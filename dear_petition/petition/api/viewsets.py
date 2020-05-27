from datetime import datetime
from django.conf import settings
from django.http import FileResponse
from django.middleware import csrf

from rest_framework import filters, parsers, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions, views as simplejwt_views

from dear_petition.users.models import User
from dear_petition.petition import models as petition
from dear_petition.petition.api import serializers
from dear_petition.petition.etl import import_ciprs_records
from dear_petition.petition.export import generate_petition_pdf

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CIPRSRecordViewSet(viewsets.ModelViewSet):

    queryset = petition.CIPRSRecord.objects.all()
    serializer_class = serializers.CIPRSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseViewSet(viewsets.ModelViewSet):
    queryset = petition.Offense.objects.all()
    serializer_class = serializers.OffenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseRecordViewSet(viewsets.ModelViewSet):
    queryset = petition.OffenseRecord.objects.all()
    serializer_class = serializers.OffenseRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):

    queryset = petition.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]


class BatchViewSet(viewsets.ModelViewSet):
    queryset = petition.Batch.objects.prefetch_related(
        "petitions", "records__offenses__offense_records"
    )
    serializer_class = serializers.BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_queryset(self):
        """ Filter queryset so that user's only have read access on objects they have created
        """
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs

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

    serializer_class = serializers.GeneratePetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        generated_petition_pdf = generate_petition_pdf(
            serializer.data["petition"], serializer.data
        )
        resp = FileResponse(generated_petition_pdf)
        resp["Content-Type"] = "application/pdf"
        resp["Content-Disposition"] = 'inline; filename="petition.pdf"'
        return resp


class TokenObtainPairCookieView(simplejwt_views.TokenObtainPairView):
    """
    Subclasses simplejwt's TokenObtainPairView to handle tokens in cookies
    """

    cookie_path = "/"

    serializer_class = serializers.TokenObtainPairCookieSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        csrf_token = csrf.get_token(self.request)

        response.set_cookie(
            settings.AUTH_COOKIE_KEY,  # get cookie key from settings
            serializer.validated_data[
                "access"
            ],  # pull access token out of validated_data
            expires=datetime.now()
            + settings.SIMPLE_JWT[
                "REFRESH_TOKEN_LIFETIME"
            ],  # expire access token when refresh token expires
            domain=getattr(
                settings, "AUTH_COOKIE_DOMAIN", None
            ),  # we can tie the cookie to a specific domain for added security
            path=self.cookie_path,
            secure=settings.DEBUG
            == False,  # browsers should only send the cookie using HTTPS
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        # We don't want 'access' or 'refresh' in response body
        response.data = {
            "detail": "success",
            "user": response.data["user"],
            "csrftoken": csrf_token,
        }

        return response

    def delete(self, request, *args, **kwargs):
        response = Response({})
        response.delete_cookie(
            settings.AUTH_COOKIE_KEY,
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
        )

        response.data = {"detail": "success"}

        return response
