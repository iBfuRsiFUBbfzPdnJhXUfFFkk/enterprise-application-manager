from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.sprint_form import SprintForm
from core.utilities.base_render import base_render


def sprint_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sprint')
    else:
        form = SprintForm()

    return base_render(
        request=request,
        template_name='authenticated/sprint/sprint_form.html',
        context={'form': form}
    )
