from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.tool_form import ToolForm
from core.models.tool import Tool
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def tool_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        tool = Tool.objects.get(id=model_id)
    except Tool.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool)
        if form.is_valid():
            form.save()
            return redirect('tool')
    else:
        form = ToolForm(instance=tool)

    return base_render(
        request=request,
        template_name='authenticated/tool/tool_form.html',
        context={'form': form}
    )
