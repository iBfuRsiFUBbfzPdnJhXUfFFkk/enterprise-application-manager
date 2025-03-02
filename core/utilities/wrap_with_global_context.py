from typing import Any, Mapping

from django.http import HttpRequest


def wrap_with_global_context(
        context: Mapping[str, Any] | None = None,
        request: HttpRequest | None = None,
) -> Mapping[str, Any]:
    if context is None:
        context = {}
    if request is None:
        return {}
    return {
        **context,
        "global_context_is_superuser": request.user.is_superuser
    }
