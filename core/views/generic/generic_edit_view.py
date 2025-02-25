from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse

from core.views.generic.generic_upsert_view import generic_upsert_view


def generic_edit_view(
        decrypt_fields: list[str] | None = None,
        form_cls: type[ModelForm] | None = None,
        model_cls: type[Model] | None = None,
        model_id: int | None = None,
        request: HttpRequest | None = None,
        success_route: str | None = None,
) -> HttpResponse:
    return generic_upsert_view(
        decrypt_fields=decrypt_fields,
        form_cls=form_cls,
        is_edit=True,
        model_cls=model_cls,
        model_id=model_id,
        request=request,
        success_route=success_route,
    )
