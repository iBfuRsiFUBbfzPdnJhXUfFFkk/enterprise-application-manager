from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.models.document import Document
from core.utilities.base_render import base_render


def bad_interaction_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES)
        if form.is_valid():
            bad_interaction = form.save()

            # If a file was uploaded, create a Document and link it
            if bad_interaction.evidence_file:
                document = Document(name=bad_interaction.get_evidence_filename())
                document.file.name = bad_interaction.evidence_file.name
                document.save()
                bad_interaction.documents.add(document)

            return redirect(to='bad_interaction')
    else:
        form = BadInteractionForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_form.html'
    )
