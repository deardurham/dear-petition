from datetime import datetime
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.http import FileResponse
import logging

from rest_framework import filters, parsers, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions, views as simplejwt_views
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from dear_petition.users.models import User
from dear_petition.petition import models as petition, utils
from dear_petition.petition.api import serializers
from dear_petition.petition.api.authentication import JWTHttpOnlyCookieAuthentication
from dear_petition.petition.etl import import_ciprs_records
from dear_petition.petition.export import generate_petition_pdf

from django_filters.rest_framework import DjangoFilterBackend


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["username"]
    ordering = ["username"]
    # TODO: Search
    # filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # search_fields = ["username"]

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == "list":
            permission_classes.append(permissions.IsAdminUser)
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        if request.user != self.get_object():
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, pk=pk)

    def perform_create(self, serializer):
        instance = serializer.save()
        form = PasswordResetForm({"email": instance.email})
        assert form.is_valid()
        form.save(
            request=self.request,
            use_https=True,
            from_email=settings.DEFAULT_FROM_EMAIL,
            email_template_name="accounts/password_setup_email.html",
        )


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

    def get(self, request):
        access_token = request.COOKIES.get(settings.AUTH_COOKIE_KEY)
        if access_token is None:
            logger.warning("Access token not found in cookie")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            validated_user, _ = JWTHttpOnlyCookieAuthentication().authenticate_token(
                access_token
            )
        except:
            validated_user = None
        if validated_user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_serializer = serializers.UserSerializer(validated_user)
        return Response({"user": user_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        # We don't want 'access' in response body
        response_data = {"detail": "success", "user": serializer.validated_data["user"]}
        response = Response(response_data, status=status.HTTP_200_OK)

        response.set_cookie(
            settings.AUTH_COOKIE_KEY,  # get cookie key from settings
            serializer.validated_data[
                "access"
            ],  # pull access token out of validated_data
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
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
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
            secure=settings.DEBUG
            == False,  # browsers should only send the cookie using HTTPS
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
            utils.remove_prefix(settings.CSRF_COOKIE_NAME, "HTTP_"),
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
        serializer = self.get_serializer(data={"refresh": refresh_key})

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
