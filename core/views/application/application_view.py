from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.views.generic.generic_view import generic_view


def application_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="applications",
        field_names=['name', '-id'],
        model_cls=Application,
        request=request,
        template_name='application.html',
    )
