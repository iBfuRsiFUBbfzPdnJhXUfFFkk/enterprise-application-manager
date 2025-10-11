from django.http import HttpRequest, HttpResponse

from core.forms.project_form import ProjectForm
from core.models.project import Project
from core.views.generic.generic_edit_view import generic_edit_view


def project_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ProjectForm,
        model_cls=Project,
        model_id=model_id,
        name='project',
        request=request,
    )
