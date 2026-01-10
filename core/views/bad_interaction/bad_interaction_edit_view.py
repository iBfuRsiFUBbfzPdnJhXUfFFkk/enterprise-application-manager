from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.models.bad_interaction import BadInteraction
from core.utilities.base_render import base_render


def bad_interaction_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)

    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES, instance=bad_interaction)
        if form.is_valid():
            form.save()
            return redirect(to='bad_interaction')
    else:
        form = BadInteractionForm(instance=bad_interaction)

    context: Mapping[str, Any] = {
        'form': form,
        'bad_interaction': bad_interaction,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_form.html'
    )
