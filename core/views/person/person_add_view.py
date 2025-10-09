from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.person_form import PersonForm
from core.utilities.base_render import base_render


def person_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='person')
    else:
        form = PersonForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/person/person_form.html'
    )
