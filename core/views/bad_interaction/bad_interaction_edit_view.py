from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.models.bad_interaction import BadInteraction
from core.models.document import Document
from core.utilities.base_render import base_render


def bad_interaction_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)

    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES, instance=bad_interaction)
        if form.is_valid():
            bad_interaction = form.save()

            # If a new file was uploaded, create a Document and link it via FK
            uploaded_file = request.FILES.get('evidence_upload')
            if uploaded_file:
                document = Document.objects.create(
                    name=uploaded_file.name,
                    version='1.0',
                    file=uploaded_file,
                )
                bad_interaction.evidence_document = document
                bad_interaction.save()

            return redirect(to='bad_interaction')
    else:
        form = BadInteractionForm(instance=bad_interaction)

    current_user_person_id = getattr(request.user, 'person_mapping_id', None)
    context: Mapping[str, Any] = {
        'form': form,
        'bad_interaction': bad_interaction,
        'current_user_person_id': current_user_person_id,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_form.html'
    )
