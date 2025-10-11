from django.http import HttpRequest, HttpResponse

from core.models.project import Project
from core.views.generic.generic_view import generic_view


def project_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Project,
        name='project',
        request=request,
    )
