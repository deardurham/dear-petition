from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import viewsets

router = routers.DefaultRouter()
router.register(r"users", viewsets.UserViewSet)
router.register(r"ciprsrecord", viewsets.CIPRSRecordViewSet)
router.register(r"offense", viewsets.OffenseViewSet)
router.register(r"offenserecord", viewsets.OffenseRecordViewSet)
router.register(r"contact", viewsets.ContactViewSet)
router.register(r"batch", viewsets.BatchViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
