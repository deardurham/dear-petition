from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views import defaults as default_views

from dear_petition.views import index

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path("petition/", include("dear_petition.petition.urls")),
    # Password Reset
    path("password_reset/", auth_views.PasswordResetView.as_view(
        subject_template_name='accounts/password_reset_subject.txt',
        email_template_name='accounts/password_reset_email.html',
    ), name='password_reset'),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # React SPA:
    path(r"", index, name="index"),
    re_path(r"^(?:.*)/?$", index, name="index-others"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
