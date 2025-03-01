from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="authenticated/home/home.html")
