from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.project_form import ProjectForm
from core.utilities.base_render import base_render


def project_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project')
    else:
        form = ProjectForm()

    return base_render(
        request=request,
        template_name='authenticated/project/project_form.html',
        context={'form': form}
    )
