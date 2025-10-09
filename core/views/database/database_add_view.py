from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.database_form import DatabaseForm
from core.utilities.base_render import base_render


def database_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DatabaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='database')
    else:
        form = DatabaseForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/database/database_form.html'
    )
