from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.policy import Policy
from core.views.generic.generic_500 import generic_500


def policy_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        policy = Policy.objects.get(id=model_id)
        policy.delete()
    except Policy.DoesNotExist:
        return generic_500(request=request)

    return redirect('policy')
