from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.server_form import ServerForm
from core.models.server import Server
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def server_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        server = Server.objects.get(id=model_id)
    except Server.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect('server')
    else:
        form = ServerForm(instance=server)

    return base_render(
        request=request,
        template_name='authenticated/server/server_form.html',
        context={'form': form}
    )
