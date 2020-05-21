from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied
from django.conf import settings

def enforce_csrf(request):
    """
    Enforce CSRF validation. From drf source, authentication.py
    """
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise PermissionDenied('CSRF validation failed: %s' % reason)

class JWTHttpOnlyCookieAuthentication(JWTAuthentication):
    # override simplejwt's authenticate method to add cookie support.
    def authenticate(self, request):
        print('!!!! HEY LOOOK HERE!!!!')
        print(request.COOKIES)
        header = self.get_header(request)
        raw_token = request.COOKIES.get(settings.AUTH_COOKIE_KEY)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)
        if not user or not user.is_active:
            return None

        enforce_csrf(request)

        return user, validated_token
