from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.models.api_authentication import APIAuthentication
from core.views.generic.generic_500 import generic_500


def api_authentication_delete_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    try:
        auth = APIAuthentication.objects.get(id=model_id)
        api_id = auth.api.id
        auth.delete()
        return redirect(to='api_detail', model_id=api_id)
    except APIAuthentication.DoesNotExist:
        return generic_500(request=request)
