from datetime import datetime
from django.conf import settings
from django.http import FileResponse

from rest_framework import filters, parsers, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions, views as simplejwt_views
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from dear_petition.users.models import User
from dear_petition.petition import models as petition, utils
from dear_petition.petition.api import serializers
from dear_petition.petition.etl import import_ciprs_records
from dear_petition.petition.export import generate_petition_pdf

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)


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
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_serializer_class(self):
        """Use a custom serializer when accessing a specific batch"""
        if self.detail:
            return serializers.BatchDetailSerializer
        return serializers.BatchSerializer

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


class GenerateDataPetitionView(viewsets.GenericViewSet):

    serializer_class = serializers.DataPetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_petition = petition.DataPetition(form_type=serializer.data["form_type"])
        generated_petition_pdf = generate_petition_pdf(
            data_petition, serializer.data["form_context"]
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

        # We don't want 'access' in response body
        response_data = { "detail": "success", "user": serializer.validated_data["user"] }
        response = Response(response_data, status=status.HTTP_200_OK)

        response.set_cookie(
            settings.AUTH_COOKIE_KEY,  # get cookie key from settings
            serializer.validated_data[
                "access"
            ],  # pull access token out of validated_data
            expires=datetime.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            domain=getattr(
                settings, "AUTH_COOKIE_DOMAIN", None
            ),  # we can tie the cookie to a specific domain for added security
            path=self.cookie_path,
            secure=settings.DEBUG
            == False,  # browsers should only send the cookie using HTTPS
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        response.set_cookie(
            settings.REFRESH_COOKIE_KEY,
            serializer.validated_data["refresh"],
            expires=datetime.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
            secure=settings.DEBUG == False,  # browsers should only send the cookie using HTTPS
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        return response

    def delete(self, request, *args, **kwargs):
        response = Response({})
        response.delete_cookie(
            settings.AUTH_COOKIE_KEY,
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
        )
        response.delete_cookie(
            settings.REFRESH_COOKIE_KEY,
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
        )
        # https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-header-name
        response.delete_cookie(
            utils.remove_prefix(settings.CSRF_COOKIE_NAME, 'HTTP_'),
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
        )

        response.data = {"detail": "success"}

        return response


class TokenRefreshCookieView(simplejwt_views.TokenRefreshView):
    cookie_path = "/"
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_key = request.COOKIES.get(settings.REFRESH_COOKIE_KEY)
        if refresh_key is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={ 'refresh': refresh_key })

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        # We don't want 'access' in response body
        response_data = {
            "detail": "success",
        }
        response = Response(response_data, status=status.HTTP_200_OK)

        response.set_cookie(
            settings.AUTH_COOKIE_KEY,  # get cookie key from settings
            serializer.validated_data[
                "access"
            ],  # pull access token out of validated_data
            expires=datetime.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            domain=getattr(
                settings, "AUTH_COOKIE_DOMAIN", None
            ),  # we can tie the cookie to a specific domain for added security
            path=self.cookie_path,
            secure=settings.DEBUG
            == False,  # browsers should only send the cookie using HTTPS
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        return response
