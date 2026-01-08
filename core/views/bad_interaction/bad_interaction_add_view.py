from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.utilities.base_render import base_render


def bad_interaction_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES)
        if form.is_valid():
            bad_interaction = form.save(commit=False)
            # Handle file upload
            if 'evidence' in request.FILES:
                uploaded_file = request.FILES['evidence']
                bad_interaction.evidence_blob_data = uploaded_file.read()
                bad_interaction.evidence_blob_filename = uploaded_file.name
                bad_interaction.evidence_blob_size = uploaded_file.size
                bad_interaction.evidence_blob_content_type = uploaded_file.content_type
            bad_interaction.save()
            return redirect(to='bad_interaction')
    else:
        form = BadInteractionForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_form.html'
    )
