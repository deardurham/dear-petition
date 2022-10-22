from django.urls import include, path
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r"users", viewsets.UserViewSet)
router.register(r"ciprsrecord", viewsets.CIPRSRecordViewSet)
router.register(r"offense", viewsets.OffenseViewSet)
router.register(r"offenserecord", viewsets.OffenseRecordViewSet)
router.register(r"contact", viewsets.ContactViewSet)
router.register(r"batch", viewsets.BatchViewSet)
router.register(r"petitions", viewsets.PetitionViewSet)
router.register(r"generatedpetition", viewsets.GeneratedPetitionViewSet)
router.register(
    r"generate-petition",
    viewsets.GeneratePetitionView,
    basename="generate-petition",
)
router.register(
    r"generate-data-petition",
    viewsets.GenerateDataPetitionView,
    basename="generate-data-petition",
)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("my-inbox/", viewsets.MyInboxView.as_view(), name="my-inbox"),
    path(
        "token/",
        ensure_csrf_cookie(viewsets.TokenObtainPairCookieView.as_view()),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        ensure_csrf_cookie(viewsets.TokenRefreshCookieView.as_view()),
        name="token_refresh",
    ),
]
