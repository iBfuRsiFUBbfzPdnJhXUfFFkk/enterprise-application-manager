from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.formula import Formula
from core.views.generic.generic_500 import generic_500


def formula_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        formula = Formula.objects.get(id=model_id)
        formula.delete()
    except Formula.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='formula')
