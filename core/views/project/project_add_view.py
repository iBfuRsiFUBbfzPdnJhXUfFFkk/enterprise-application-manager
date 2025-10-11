from django.http import HttpRequest, HttpResponse

from core.forms.project_form import ProjectForm
from core.models.project import Project
from core.views.generic.generic_add_view import generic_add_view


def project_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ProjectForm,
        model_cls=Project,
        name='project',
        request=request,
    )
