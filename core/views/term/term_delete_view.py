from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.term import Term
from core.views.generic.generic_500 import generic_500


def term_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        term = Term.objects.get(id=model_id)
        term.delete()
    except Term.DoesNotExist:
        return generic_500(request=request)

    return redirect('term')
