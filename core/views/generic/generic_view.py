from typing import Any, Mapping

from django.db.models import Model, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.views.generic.generic_500 import generic_500


def generic_view(
        context_name: str | None = None,
        model_cls: type[Model] | None = None,
        request: HttpRequest | None = None,
        template_name: str | None = None,
        additional_context: Mapping[str, Any] | None = None,
) -> HttpResponse:
    if context_name is None:
        return generic_500(request=request)
    if model_cls is None:
        return generic_500(request=request)
    if request is None:
        return generic_500(request=request)
    if template_name is None:
        return generic_500(request=request)
    models: QuerySet = model_cls.objects.all()
    additional_context: Mapping[str, Any] = additional_context or {}
    context: Mapping[str, Any] = {**additional_context, context_name: models}
    return render(context=context, request=request, template_name=template_name)
