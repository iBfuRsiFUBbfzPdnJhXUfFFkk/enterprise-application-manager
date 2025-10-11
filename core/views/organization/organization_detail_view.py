from django.http import HttpRequest, HttpResponse

from core.models.organization import Organization
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def organization_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        organization = Organization.objects.get(id=model_id)
        historical_records = organization.history.all()
    except Organization.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/organization/organization_detail.html',
        context={
            'organization': organization,
            'historical_records': historical_records,
        }
    )
