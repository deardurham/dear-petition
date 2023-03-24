import csv
import logging
import tempfile

from django.db import transaction
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import update_last_login
from django.http import FileResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, parsers, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt import views as simplejwt_views
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from dear_petition.petition import constants
from dear_petition.petition import models as pm
from dear_petition.petition import utils
from dear_petition.petition.api import serializers
from dear_petition.petition.api.authentication import JWTHttpOnlyCookieAuthentication
from dear_petition.petition.etl import (
    import_ciprs_records,
    recalculate_petitions,
    assign_agencies_to_documents,
)
from dear_petition.petition.export import generate_petition_pdf
from dear_petition.users.models import User
from dear_petition.petition.export.documents.advice_letter import (
    generate_advice_letter as generate_advice_letter,
)
from dear_petition.petition.export.documents.expungable_summary import (
    generate_expungable_summary as generate_expungable_summary,
)

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["username", "email", "last_login"]
    ordering = ["username"]
    search_fields = ["username", "email"]

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

    queryset = pm.CIPRSRecord.objects.all()
    serializer_class = serializers.CIPRSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseViewSet(viewsets.ModelViewSet):
    queryset = pm.Offense.objects.all()
    serializer_class = serializers.OffenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffenseRecordViewSet(viewsets.ModelViewSet):
    queryset = pm.OffenseRecord.objects.all()
    serializer_class = serializers.OffenseRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=["get"],
    )
    def get_petition_records(self, request):
        petition_id = request.GET.get("petition")
        if not petition_id:
            return Response(
                "No petition id provided.", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pet = pm.Petition.objects.get(id=petition_id)
        except pm.Petition.DoesNotExist:
            return Response(
                "Petition with this id does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        offense_records = pet.get_all_offense_records(filter_active=False)
        active_records = list(
            offense_records.filter(petitionoffenserecord__active=True).values_list(
                "id", flat=True
            )
        )
        serialized_data = {
            "offense_records": self.get_serializer(offense_records, many=True).data,
            "active_records": active_records,
        }

        return Response(serialized_data)


class ContactSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_field = request.query_params.get("field", None)
        if search_field is not None:
            return [search_field]
        return super().get_search_fields(view, request)


class ContactViewSet(viewsets.ModelViewSet):

    queryset = pm.Contact.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, ContactSearchFilter]
    filterset_fields = {
        "category": ["exact"],
        "city": ["exact", "in"],
        "zipcode": ["exact", "in"],
    }
    search_fields = ["name"]
    ordering_fields = ["name", "address1", "address2", "city", "zipcode"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.request.data.get('category') == 'client':
            return serializers.ClientSerializer
        return serializers.ContactSerializer

    def get_queryset(self):
        if self.request.query_params.get('category') == 'client' or self.request.data.get('category') == 'client':
            return pm.Contact.objects.filter(user=self.request.user)
        return pm.Contact.objects.all()

    def perform_create(self, serializer):
        if self.request.query_params.get('category') == 'client' or self.request.data.get('category') == 'client':
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=False, methods=["get"])
    def get_filter_options(self, request):
        field = request.query_params.get("field", None)
        if field is None or field not in self.filterset_fields:
            return Response(
                "Provided field is not a valid filter field",
                status=status.HTTP_400_BAD_REQUEST,
            )
        field_options = (
            self.filter_queryset(self.get_queryset())
            .values_list(field, flat=True)
            .distinct()
            .order_by()
        )
        return Response(field_options)


class BatchViewSet(viewsets.ModelViewSet):
    queryset = pm.Batch.objects.prefetch_related(
        "petitions", "records__offenses__offense_records"
    )
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['user']
    ordering_fields = ['date_uploaded']
    ordering = ['-date_uploaded']

    def get_serializer_class(self):
        """Use a custom serializer when accessing a specific batch"""
        if self.detail:
            return serializers.BatchDetailSerializer
        return serializers.BatchSerializer

    def get_queryset(self):
        """Filter queryset so that user's only have read access on objects they have created"""
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
        parser_mode = serializer.data["parser_mode"]
        batch = import_ciprs_records(
            files=files, user=self.request.user, parser_mode=parser_mode
        )
        return {"id": batch.pk}

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=[
            "post",
        ],
    )
    def generate_advice_letter(self, request, pk):
        batch = self.get_object()
        errors = {}
        if batch.attorney is None:
            errors['attorney'] = ['This field is required']
        if batch.client is None:
            errors['client'] = ['This field is required']
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = tmpdir + "/advice_letter.docx"
            advice_letter = generate_advice_letter(batch)
            advice_letter.save(filepath)
            resp = FileResponse(open(filepath, "rb"))
            resp[
                "Content-Type"
            ] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            resp["Content-Disposition"] = 'attachment; filename="Advice Letter.docx"'
            return resp

    @action(
        detail=True,
        methods=[
            "post",
        ],
    )
    def generate_expungable_summary(self, request, pk):
        batch = self.get_object()
        errors = {}
        if batch.attorney is None:
            errors['attorney'] = ['This field is required']
        if batch.client is None:
            errors['client'] = ['This field is required']
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = tmpdir + "/expungable_summary.docx"
            expungable_summary = generate_expungable_summary(batch)
            expungable_summary.save(filepath)
            resp = FileResponse(open(filepath, "rb"))
            resp[
                "Content-Type"
            ] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            resp["Content-Disposition"] = 'attachment; filename="Expungable Record Summary.docx"'
            return resp


class MyInboxView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MyInboxSerializer

    def get_queryset(self):
        return (
            pm.Batch.objects.filter(user=self.request.user)
            .annotate(total_files=Count("files"), total_emails=Count("emails"))
            .order_by("-date_uploaded")
        )


class PetitionViewSet(viewsets.ModelViewSet):
    queryset = pm.Petition.objects.all()
    serializer_class = serializers.ParentPetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        detail=True,
        methods=[
            "post",
        ],
    )
    def recalculate_petitions(self, request, pk):
        data = request.data

        offense_record_ids = data["offense_record_ids"]

        if not isinstance(offense_record_ids, list):
            return Response(
                "Provided offense record ids should be a list.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_petition = recalculate_petitions(pk, offense_record_ids)

        new_petition = self.get_serializer(new_petition)

        return Response(new_petition.data, status=200)

    @action(
        detail=True,
        methods=[
            "post",
        ],
    )
    def assign_agencies_to_documents(self, request, pk):
        data = request.data
        agencies = data["agencies"]
        agency_ids = [agency["pk"] for agency in agencies]

        with transaction.atomic():
            petition = pm.Petition.objects.get(id=pk)
            petition.agencies.clear()
            for agency_id in agency_ids:
                petition.agencies.add(agency_id)
            petition = assign_agencies_to_documents(petition)

        petition = self.get_serializer(petition)

        return Response(petition.data, status=200)

    @action(detail=True, methods=["post"])
    def generate_petition_pdf(self, request, pk=None):
        serializer = serializers.GeneratePetitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        petition = self.get_object()
        client = petition.batch.client

        petition_documents = pm.PetitionDocument.objects.filter(
            petition=pk, pk__in=serializer.data["documents"]
        ).order_by("pk")
        assert (
            len(petition_documents) > 0
        ), "Petition documents could not be found for petition"

        form_context = serializer.validated_data.copy()
        form_context['client'] = client
        form_context['attorney'] = petition.batch.attorney
        form_context['agencies'] = petition.agencies
        generated_petition_pdf = generate_petition_pdf(
            petition_documents, form_context
        )

        for doc in petition_documents.iterator():
            pm.GeneratedPetition.get_stats_generated_petition(doc.pk, request.user)

        resp = FileResponse(generated_petition_pdf)
        resp["Content-Type"] = "application/pdf"

        petition = self.get_object()
        filename = f'{client.name} - {petition.form_type} - {petition.jurisdiction} {petition.county}.pdf'
        resp["Content-Disposition"] = f'inline; filename="{filename}"'

        return resp


class GenerateDataPetitionView(viewsets.ModelViewSet):

    serializer_class = serializers.DataPetitionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_petition = pm.DataPetition(form_type=serializer.data["form_type"])
        generated_petition_pdf = generate_petition_pdf(
            data_petition, serializer.data["form_context"]
        )
        resp = FileResponse(generated_petition_pdf)
        resp["Content-Type"] = "application/pdf"
        resp["Content-Disposition"] = 'inline; filename="petition.pdf"'
        return resp


class GeneratedPetitionViewSet(viewsets.GenericViewSet):

    queryset = pm.GeneratedPetition.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @action(
        detail=False,
        methods=[
            "get",
        ],
    )
    def download_as_csv(self, request):
        model_fields = pm.GeneratedPetition._meta.fields
        field_names = [
            field.name
            for field in model_fields
            if field.name in constants.GENERATED_PETITION_ADMIN_FIELDS
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        writer = csv.writer(response, delimiter=";")

        writer.writerow(field_names)

        for row in self.queryset:
            values = []
            for field in field_names:
                value = getattr(row, field)
                if value is None:
                    value = ""
                values.append(value)
            writer.writerow(values)
        return response


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

        update_last_login(None, validated_user)
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
            secure=settings.DEBUG is False,
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        response.set_cookie(
            settings.REFRESH_COOKIE_KEY,
            serializer.validated_data["refresh"],
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            domain=getattr(settings, "AUTH_COOKIE_DOMAIN", None),
            path=self.cookie_path,
            secure=settings.DEBUG is False,
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
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            domain=getattr(
                settings, "AUTH_COOKIE_DOMAIN", None
            ),  # we can tie the cookie to a specific domain for added security
            path=self.cookie_path,
            secure=settings.DEBUG is False,
            httponly=True,  # browsers should not allow javascript access to this cookie
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        return response
