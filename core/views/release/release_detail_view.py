from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.release import Release
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def release_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        release = Release.objects.get(id=model_id)
    except Release.DoesNotExist:
        return generic_500(request=request)

    created_record = release.history.order_by('history_date').first()
    updated_record = release.history.order_by('-history_date').first()

    context: Mapping[str, Any] = {
        'model': release,
        'created_record': created_record,
        'updated_record': updated_record,
    }
    return base_render(context=context, request=request,
                      template_name='authenticated/release/release_detail.html')
