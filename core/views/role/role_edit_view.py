from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.role_form import RoleForm
from core.models.role import Role
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def role_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        role = Role.objects.get(id=model_id)
    except Role.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role')
    else:
        form = RoleForm(instance=role)

    return base_render(
        request=request,
        template_name='authenticated/role/role_form.html',
        context={'form': form}
    )
