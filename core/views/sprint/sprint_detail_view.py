from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def sprint_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        sprint = Sprint.objects.get(id=model_id)
        historical_records = sprint.history.all()
    except Sprint.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/sprint/sprint_detail.html',
        context={
            'sprint': sprint,
            'historical_records': historical_records,
        }
    )
