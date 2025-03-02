from typing import Sequence, Any, Mapping

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from core.utilities.wrap_with_global_context import wrap_with_global_context


def base_render(
        content_type: str | None = None,
        context: Mapping[str, Any] | None = None,
        request: HttpRequest | None = None,
        status: int | None = None,
        template_name: str | Sequence[str] | None = None,
        using: str | None = None,
) -> HttpResponse:
    return render(
        content_type=content_type,
        context=wrap_with_global_context(context=context, request=request),
        request=request,
        status=status,
        template_name=template_name or [],
        using=using,
    )
