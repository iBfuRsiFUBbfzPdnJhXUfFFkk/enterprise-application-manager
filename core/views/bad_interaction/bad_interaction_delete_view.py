from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.bad_interaction import BadInteraction


def bad_interaction_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)
    bad_interaction.delete()
    return redirect(to='bad_interaction')
