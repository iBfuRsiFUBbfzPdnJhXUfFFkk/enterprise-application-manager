from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.dependency_form import DependencyForm
from core.models.dependency import Dependency
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def dependency_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        dependency = Dependency.objects.get(id=model_id)
    except Dependency.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DependencyForm(request.POST, instance=dependency)
        if form.is_valid():
            form.save()
            return redirect(to='dependency')
    else:
        form = DependencyForm(instance=dependency)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/dependency/dependency_form.html'
    )
