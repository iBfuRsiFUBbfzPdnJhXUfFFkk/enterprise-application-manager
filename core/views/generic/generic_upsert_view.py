from typing import Mapping, Any

from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.views.generic.generic_500 import generic_500


def generic_upsert_view(
        decrypt_fields: list[str] | None = None,
        form_cls: type[ModelForm] | None = None,
        is_edit: bool | None = None,
        model_cls: type[Model] | None = None,
        model_id: int | None = None,
        request: HttpRequest | None = None,
        success_route: str | None = None,
) -> HttpResponse:
    if is_edit is None:
        is_edit = False
    if form_cls is None:
        return generic_500(request=request)
    if model_cls is None and is_edit:
        return generic_500(request=request)
    if model_id is None and is_edit:
        return generic_500(request=request)
    if request is None:
        return generic_500(request=request)
    if success_route is None:
        return generic_500(request=request)
    method: str | None = request.method
    if method is None:
        return generic_500(request=request)
    immutable_query_dict = request.POST
    if is_edit:
        model_instance: Model | None = model_cls.objects.get(id=model_id)
        if decrypt_fields is not None:
            for field in decrypt_fields:
                decrypted_value: str = getattr(model_instance, f"get_{field}")()
                setattr(model_instance, field, decrypted_value)
    else:
        model_instance = None
    if method == 'POST':
        form: ModelForm = form_cls(immutable_query_dict, instance=model_instance)
        is_valid: bool = form.is_valid()
        if is_valid:
            form.save()
            return redirect(to=success_route)
    else:
        form: ModelForm = form_cls(instance=model_instance)
    context: Mapping[str, Any] = {'form': form}
    return render(
        context=context,
        request=request,
        template_name='generic_edit.html' if is_edit else 'generic_add.html'
    )
