from django.http import HttpRequest, HttpResponse

from core.models.role import Role
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def role_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        role = Role.objects.get(id=model_id)
        historical_records = role.history.all()
    except Role.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/role/role_detail.html',
        context={
            'role': role,
            'historical_records': historical_records,
        }
    )
