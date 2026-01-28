from datetime import date
from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.bad_interaction_form import BadInteractionForm
from core.models.document import Document
from core.utilities.base_render import base_render


def bad_interaction_add_view(request: HttpRequest) -> HttpResponse:
    current_user_person_id = getattr(request.user, 'person_mapping_id', None)

    if request.method == 'POST':
        form = BadInteractionForm(request.POST, request.FILES)
        if form.is_valid():
            bad_interaction = form.save()

            # If a file was uploaded, create a Document and link it via FK
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
        initial = {
            'reported_by': current_user_person_id,
            'severity': 'MEDIUM',
            'date_occurred': date.today(),
        }
        form = BadInteractionForm(initial=initial)

    context: Mapping[str, Any] = {
        'form': form,
        'current_user_person_id': current_user_person_id,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_form.html'
    )
