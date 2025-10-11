from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.link import Link
from core.views.generic.generic_500 import generic_500


def link_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        link = Link.objects.get(id=model_id)
        link.delete()
    except Link.DoesNotExist:
        return generic_500(request=request)

    return redirect('link')
