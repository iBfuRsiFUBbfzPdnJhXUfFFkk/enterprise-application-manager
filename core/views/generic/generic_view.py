from typing import Any, Mapping

from django.db.models import Model, QuerySet
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def generic_view(
        additional_context: Mapping[str, Any] | None = None,
        model_cls: type[Model] | None = None,
        name: str | None = None,
        request: HttpRequest | None = None,
) -> HttpResponse:
    if model_cls is None:
        return generic_500(request=request)
    if request is None:
        return generic_500(request=request)
    if name is None:
        return generic_500(request=request)
    models: QuerySet = model_cls.objects.all()
    additional_context: Mapping[str, Any] = additional_context or {}
    context: Mapping[str, Any] = {**additional_context, "models": models}
    return base_render(
        context=context,
        request=request,
        template_name=f"authenticated/{name}/{name}.html"
    )
