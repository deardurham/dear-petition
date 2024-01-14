from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import (
    CSRFCheck,
    SessionAuthentication as DRFSessionAuthentication,
)
from rest_framework.exceptions import NotAuthenticated
from django.conf import settings


def enforce_csrf(request):
    """
    Enforce CSRF validation. From drf source, authentication.py
    """

    def dummy_get_response(request):  # pragma: no cover
        return None

    check = CSRFCheck(dummy_get_response)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise NotAuthenticated("CSRF validation failed: %s" % reason)


class JWTHttpOnlyCookieAuthentication(JWTAuthentication):
    # override simplejwt's authenticate method to add cookie support.

    def _validate_token(self, token):
        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)
        if not user or not user.is_active:
            return None
        return user, validated_token

    def authenticate(self, request):
        raw_token = request.COOKIES.get(settings.AUTH_COOKIE_KEY)
        if raw_token is None:
            return None
        validated_user, validated_token = self.authenticate_token(raw_token)

        enforce_csrf(request)

        return validated_user, validated_token

    def authenticate_token(self, token):
        validated_user, validated_token = self._validate_token(token)
        if not validated_user and validated_token:
            return None

        return validated_user, validated_token


# Lifted from csdenboer's suggestion on Github: https://github.com/encode/django-rest-framework/issues/5968#issuecomment-399352828
class SessionAuthentication(DRFSessionAuthentication):
    """
    This class is needed, because REST Framework's default SessionAuthentication does never return 401's,
    because they cannot fill the WWW-Authenticate header with a valid value in the 401 response. As a
    result, we cannot distinguish calls that are not unauthorized (401 unauthorized) and calls for which
    the user does not have permission (403 forbidden). See https://github.com/encode/django-rest-framework/issues/5968

    We do set authenticate_header function in SessionAuthentication, so that a value for the WWW-Authenticate
    header can be retrieved and the response code is automatically set to 401 in case of unauthenticated requests.
    """

    def authenticate_header(self, request):
        return "Session"
