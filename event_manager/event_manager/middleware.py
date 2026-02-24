
from event_manager.current_user import set_current_user


class CurrentUserMiddleware:


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            set_current_user(user)
        else:
            set_current_user(None)
        try:
            return self.get_response(request)
        finally:
            set_current_user(None)

    def process_exception(self, request, exception):
        set_current_user(None)
