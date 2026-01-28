from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.hr_incident_update_form import HRIncidentUpdateForm
from core.models.document import Document
from core.models.hr_incident import HRIncident


def hr_incident_add_update_view(request: HttpRequest, model_id: int) -> HttpResponse:
    hr_incident = get_object_or_404(HRIncident, pk=model_id)

    if request.method == 'POST':
        form = HRIncidentUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.hr_incident = hr_incident
            update.created_by = request.user
            update.save()

            # If a file was uploaded, create a Document and link it via FK
            uploaded_file = request.FILES.get('attachment_upload')
            if uploaded_file:
                document = Document.objects.create(
                    name=uploaded_file.name,
                    version='1.0',
                    file=uploaded_file,
                )
                update.attachment_document = document
                update.save()

            return redirect('hr_incident_detail', model_id=model_id)

    # If GET or form invalid, redirect back to detail page
    return redirect('hr_incident_detail', model_id=model_id)
