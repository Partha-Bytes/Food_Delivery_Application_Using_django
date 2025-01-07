# your_app/middleware.py

from django.contrib.auth import logout

class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log out the user for every request
        if request.user.is_authenticated:
            logout(request)  # This logs the user out
        response = self.get_response(request)
        return response
