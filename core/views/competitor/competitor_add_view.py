from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.competitor_form import CompetitorForm
from core.utilities.base_render import base_render


def competitor_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CompetitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('competitor')
    else:
        form = CompetitorForm()

    return base_render(
        request=request,
        template_name='authenticated/competitor/competitor_form.html',
        context={'form': form}
    )
