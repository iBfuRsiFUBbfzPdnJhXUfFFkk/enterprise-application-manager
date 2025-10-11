from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.term_form import TermForm
from core.utilities.base_render import base_render


def term_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('term')
    else:
        form = TermForm()

    return base_render(
        request=request,
        template_name='authenticated/term/term_form.html',
        context={'form': form}
    )
