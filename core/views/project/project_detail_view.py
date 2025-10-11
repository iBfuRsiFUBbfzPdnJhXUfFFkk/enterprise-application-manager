from django.http import HttpRequest, HttpResponse

from core.models.project import Project
from core.views.generic.generic_detail_view import generic_detail_view


def project_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_detail_view(
        model_cls=Project,
        model_id=model_id,
        name='project',
        request=request,
    )
