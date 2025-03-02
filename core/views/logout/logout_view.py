from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect(to='login')
