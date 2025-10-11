from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.project_form import ProjectForm
from core.models.project import Project
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def project_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        project = Project.objects.get(id=model_id)
    except Project.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project')
    else:
        form = ProjectForm(instance=project)

    return base_render(
        request=request,
        template_name='authenticated/project/project_form.html',
        context={'form': form}
    )
