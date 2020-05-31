from django.urls import path, include

urlpatterns = [
    path("api/", include("dear_petition.petition.api.urls", namespace="api")),
]
