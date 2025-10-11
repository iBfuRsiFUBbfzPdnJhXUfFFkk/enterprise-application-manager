from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.role import Role
from core.views.generic.generic_500 import generic_500


def role_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        role = Role.objects.get(id=model_id)
        role.delete()
    except Role.DoesNotExist:
        return generic_500(request=request)

    return redirect('role')
