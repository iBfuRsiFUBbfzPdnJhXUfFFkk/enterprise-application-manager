from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.views.generic.generic_500 import generic_500


def generic_delete_view(
        model_cls: type[Model] | None = None,
        model_id: int | None = None,
        request: HttpRequest | None = None,
        success_route: str | None = None,
) -> HttpResponse:
    if model_cls is None:
        return generic_500(request=request)
    if model_id is None:
        return generic_500(request=request)
    if request is None:
        return generic_500(request=request)
    if success_route is None:
        return generic_500(request=request)

    try:
        model_instance: Model = model_cls.objects.get(id=model_id)
        model_instance.delete()
        return redirect(to=success_route)
    except model_cls.DoesNotExist:
        return generic_500(request=request)
