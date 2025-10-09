from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.dependency_form import DependencyForm
from core.utilities.base_render import base_render


def dependency_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DependencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='dependency')
    else:
        form = DependencyForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/dependency/dependency_form.html'
    )
