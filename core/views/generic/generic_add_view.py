from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse

from core.views.generic.generic_upsert_view import generic_upsert_view


def generic_add_view(
        form_cls: type[ModelForm] | None = None,
        request: HttpRequest | None = None,
        success_route: str | None = None,
) -> HttpResponse:
    return generic_upsert_view(
        form_cls=form_cls,
        request=request,
        success_route=success_route,
    )
