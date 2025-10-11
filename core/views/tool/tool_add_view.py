from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.tool_form import ToolForm
from core.utilities.base_render import base_render


def tool_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tool')
    else:
        form = ToolForm()

    return base_render(
        request=request,
        template_name='authenticated/tool/tool_form.html',
        context={'form': form}
    )
