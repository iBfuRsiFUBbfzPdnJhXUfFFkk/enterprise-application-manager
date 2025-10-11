from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.role_form import RoleForm
from core.utilities.base_render import base_render


def role_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role')
    else:
        form = RoleForm()

    return base_render(
        request=request,
        template_name='authenticated/role/role_form.html',
        context={'form': form}
    )
