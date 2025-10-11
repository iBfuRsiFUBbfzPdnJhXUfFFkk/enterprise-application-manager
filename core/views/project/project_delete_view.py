from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.project import Project
from core.views.generic.generic_500 import generic_500


def project_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        project = Project.objects.get(id=model_id)
        project.delete()
    except Project.DoesNotExist:
        return generic_500(request=request)

    return redirect('project')
