from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def generic_500(request: HttpRequest | None = None) -> HttpResponse:
    return render(
        request=request,
        status=500,
        template_name='500.html',
    )
