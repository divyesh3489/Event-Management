from rest_framework_simplejwt.authentication import JWTAuthentication
from event_manager.current_user import set_current_user


class JWTAuthenticationWithCurrentUser(JWTAuthentication):
    """
    JWT authentication that sets the current user in context so middleware-style
    logic (e.g. base model created_by/updated_by) works in API views.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, _ = result
            set_current_user(user)
        return result
