from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.term_form import TermForm
from core.models.term import Term
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def term_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        term = Term.objects.get(id=model_id)
    except Term.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('term')
    else:
        form = TermForm(instance=term)

    return base_render(
        request=request,
        template_name='authenticated/term/term_form.html',
        context={'form': form}
    )
