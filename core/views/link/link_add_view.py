from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.link_form import LinkForm
from core.utilities.base_render import base_render


def link_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('link')
    else:
        form = LinkForm()

    return base_render(
        request=request,
        template_name='authenticated/link/link_form.html',
        context={'form': form}
    )
