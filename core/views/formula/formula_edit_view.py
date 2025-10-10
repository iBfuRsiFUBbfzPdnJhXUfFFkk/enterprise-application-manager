from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.formula_form import FormulaForm
from core.models.formula import Formula
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def formula_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        formula = Formula.objects.get(id=model_id)
    except Formula.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = FormulaForm(request.POST, instance=formula)
        if form.is_valid():
            form.save()
            return redirect(to='formula')
    else:
        form = FormulaForm(instance=formula)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/formula/formula_form.html'
    )
