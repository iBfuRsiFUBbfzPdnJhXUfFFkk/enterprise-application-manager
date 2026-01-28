from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.models.bad_interaction import BadInteraction
from core.models.document import Document
from core.utilities.base_render import base_render


def bad_interaction_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)
    old_evidence_file_name = bad_interaction.evidence_file.name if bad_interaction.evidence_file else None

    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES, instance=bad_interaction)
        if form.is_valid():
            bad_interaction = form.save()

            # If a new file was uploaded, create a Document and link it
            new_file_name = bad_interaction.evidence_file.name if bad_interaction.evidence_file else None
            if new_file_name and new_file_name != old_evidence_file_name:
                document = Document(name=bad_interaction.get_evidence_filename())
                document.file.name = bad_interaction.evidence_file.name
                document.save()
                bad_interaction.documents.add(document)

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
