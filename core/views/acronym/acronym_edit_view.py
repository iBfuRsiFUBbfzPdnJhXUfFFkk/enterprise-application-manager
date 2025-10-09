from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.acronym_form import AcronymForm
from core.models.acronym import Acronym
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def acronym_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        acronym = Acronym.objects.get(id=model_id)
    except Acronym.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = AcronymForm(request.POST, instance=acronym)
        if form.is_valid():
            form.save()
            return redirect(to='acronym')
    else:
        form = AcronymForm(instance=acronym)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/acronym/acronym_form.html'
    )
