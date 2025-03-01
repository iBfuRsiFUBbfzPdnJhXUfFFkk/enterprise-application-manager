from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationRequiredMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/authenticated/') and not request.user.is_authenticated:
            return redirect(to=reverse(viewname='login'))
        return self.get_response(request)