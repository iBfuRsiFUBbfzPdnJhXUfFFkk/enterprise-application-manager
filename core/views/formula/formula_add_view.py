from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.formula_form import FormulaForm
from core.utilities.base_render import base_render


def formula_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FormulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='formula')
    else:
        form = FormulaForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/formula/formula_form.html'
    )
