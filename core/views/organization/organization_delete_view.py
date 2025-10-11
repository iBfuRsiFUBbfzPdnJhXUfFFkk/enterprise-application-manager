from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.organization import Organization
from core.views.generic.generic_500 import generic_500


def organization_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        organization = Organization.objects.get(id=model_id)
        organization.delete()
    except Organization.DoesNotExist:
        return generic_500(request=request)

    return redirect('organization')
