from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.server_form import ServerForm
from core.utilities.base_render import base_render


def server_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('server')
    else:
        form = ServerForm()

    return base_render(
        request=request,
        template_name='authenticated/server/server_form.html',
        context={'form': form}
    )
