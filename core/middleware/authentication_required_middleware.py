from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/authenticated/') and not request.user.is_authenticated:
            return redirect(reverse('login'))
        response = self.get_response(request)
        return response