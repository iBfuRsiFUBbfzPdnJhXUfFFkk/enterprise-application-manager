from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.application import Application
from core.views.generic.generic_delete_view import generic_delete_view


def application_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_delete_view(
        model_cls=Application,
        model_id=model_id,
        request=request,
        success_route='application',
    )
