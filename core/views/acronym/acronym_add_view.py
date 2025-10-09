from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.acronym_form import AcronymForm
from core.utilities.base_render import base_render


def acronym_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AcronymForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='acronym')
    else:
        form = AcronymForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/acronym/acronym_form.html'
    )
