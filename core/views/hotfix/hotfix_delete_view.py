from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.hotfix import Hotfix
from core.views.generic.generic_500 import generic_500


def hotfix_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        hotfix = Hotfix.objects.get(id=model_id)
        hotfix.delete()
    except Hotfix.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='hotfix')
