from django.http import HttpRequest, HttpResponse

from core.models.policy import Policy
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def policy_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        policy = Policy.objects.get(id=model_id)
        historical_records = policy.history.all()
    except Policy.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/policy/policy_detail.html',
        context={
            'policy': policy,
            'historical_records': historical_records,
        }
    )
