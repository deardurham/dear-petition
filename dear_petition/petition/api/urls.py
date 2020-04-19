from django.urls import include, path
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r"users", viewsets.UserViewSet)
router.register(r"ciprsrecord", viewsets.CIPRSRecordViewSet)
router.register(r"contact", viewsets.ContactViewSet)
router.register(r"batch", viewsets.BatchViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
