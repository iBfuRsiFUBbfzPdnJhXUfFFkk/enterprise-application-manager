from django.http import HttpRequest, HttpResponse

from core.models.project import Project
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def project_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        project = Project.objects.get(id=model_id)
        historical_records = project.history.all()
    except Project.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/project/project_detail.html',
        context={
            'project': project,
            'historical_records': historical_records,
        }
    )
