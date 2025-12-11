from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class AuthenticationRequiredMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/authenticated/') and not request.user.is_authenticated:
            # For AJAX requests, return JSON error instead of redirect
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               request.content_type == 'application/json' or \
               'application/json' in request.headers.get('Accept', ''):
                return JsonResponse(
                    {'success': False, 'error': 'Authentication required'},
                    status=401
                )
            return redirect(to=reverse(viewname='login'))
        return self.get_response(request)
