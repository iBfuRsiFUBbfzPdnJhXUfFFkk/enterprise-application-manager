from django.http import HttpRequest, HttpResponse

from core.models.project import Project
from core.views.generic.generic_delete_view import generic_delete_view


def project_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_delete_view(
        model_cls=Project,
        model_id=model_id,
        name='project',
        request=request,
    )
