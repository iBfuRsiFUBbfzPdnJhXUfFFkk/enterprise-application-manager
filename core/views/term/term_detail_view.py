from django.http import HttpRequest, HttpResponse

from core.models.acronym import Acronym
from core.models.term import Term
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def term_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        term = Term.objects.get(id=model_id)
        historical_records = term.history.all()
    except Term.DoesNotExist:
        return generic_500(request=request)

    try:
        linked_acronym = term.acronym
    except Acronym.DoesNotExist:
        linked_acronym = None

    return base_render(
        request=request,
        template_name='authenticated/term/term_detail.html',
        context={
            'term': term,
            'historical_records': historical_records,
            'linked_acronym': linked_acronym,
        }
    )
