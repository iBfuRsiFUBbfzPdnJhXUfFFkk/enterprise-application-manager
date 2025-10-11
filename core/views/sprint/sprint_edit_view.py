from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.sprint_form import SprintForm
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def sprint_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        sprint = Sprint.objects.get(id=model_id)
    except Sprint.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = SprintForm(request.POST, instance=sprint)
        if form.is_valid():
            form.save()
            return redirect('sprint')
    else:
        form = SprintForm(instance=sprint)

    return base_render(
        request=request,
        template_name='authenticated/sprint/sprint_form.html',
        context={'form': form}
    )
