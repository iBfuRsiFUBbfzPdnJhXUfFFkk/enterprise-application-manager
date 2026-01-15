from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.database_form import DatabaseForm
from core.models.database import Database
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def database_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        database = Database.objects.get(id=model_id)
    except Database.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DatabaseForm(request.POST, request.FILES, instance=database)
        if form.is_valid():
            form.save()
            return redirect(to='database_detail', model_id=database.id)
    else:
        form = DatabaseForm(instance=database)

    context: Mapping[str, Any] = {
        'form': form,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/database/database_form.html'
    )
