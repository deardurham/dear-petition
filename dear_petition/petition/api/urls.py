from django.urls import include, path
from rest_framework import routers
from . import viewsets
from dear_petition.petition.api import authentication

router = routers.DefaultRouter()
router.register(r"users", viewsets.UserViewSet)
router.register(r"ciprsrecord", viewsets.CIPRSRecordViewSet)
router.register(r"offense", viewsets.OffenseViewSet)
router.register(r"offenserecord", viewsets.OffenseRecordViewSet)
router.register(r"contact", viewsets.ContactViewSet)
router.register(r"batch", viewsets.BatchViewSet)
router.register(
    r"generate-petition", viewsets.GeneratePetitionView, basename="generate-petition",
)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("token/", viewsets.TokenObtainPairCookieView.as_view(), name="token_obtain_pair"),
]
