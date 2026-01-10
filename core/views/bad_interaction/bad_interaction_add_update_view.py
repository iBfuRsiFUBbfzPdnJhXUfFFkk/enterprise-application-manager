from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.bad_interaction_update_form import BadInteractionUpdateForm
from core.models.bad_interaction import BadInteraction


def bad_interaction_add_update_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)

    if request.method == 'POST':
        form = BadInteractionUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.bad_interaction = bad_interaction
            update.created_by = request.user
            update.save()
            return redirect('bad_interaction_detail', model_id=model_id)

    # If GET or form invalid, redirect back to detail page
    return redirect('bad_interaction_detail', model_id=model_id)
