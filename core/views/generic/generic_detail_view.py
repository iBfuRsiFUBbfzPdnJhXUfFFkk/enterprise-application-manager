from typing import Any, Mapping

from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from core.views.generic.generic_500 import generic_500


def generic_detail_view(
        additional_context: Mapping[str, Any] | None = None,
        model_cls: type[Model] | None = None,
        model_id: int | None = None,
        request: HttpRequest | None = None,
        template_name: str | None = None,
) -> HttpResponse:
    if model_cls is None:
        return generic_500(request=request)
    if model_id is None:
        return generic_500(request=request)
    if request is None:
        return generic_500(request=request)
    if template_name is None:
        return generic_500(request=request)
    model: model_cls = get_object_or_404(klass=model_cls, pk=model_id)
    additional_context: Mapping[str, Any] = additional_context or {}
    context: Mapping[str, Any] = {**additional_context, "model": model}
    return render(context=context, request=request, template_name=template_name)
