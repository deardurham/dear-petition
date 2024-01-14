from django.urls import path

from . import views

urlpatterns = [
    path("bookmarklet/", views.bookmarklet_handler, name="portal-bookmarklet-handler"),
]
