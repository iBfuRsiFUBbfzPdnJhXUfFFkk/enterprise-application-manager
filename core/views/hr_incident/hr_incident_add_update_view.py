from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.hr_incident_update_form import HRIncidentUpdateForm
from core.models.hr_incident import HRIncident


def hr_incident_add_update_view(request: HttpRequest, model_id: int) -> HttpResponse:
    hr_incident = get_object_or_404(HRIncident, pk=model_id)

    if request.method == 'POST':
        form = HRIncidentUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.hr_incident = hr_incident
            update.created_by = request.user

            # Handle file upload
            if 'attachment' in request.FILES:
                uploaded_file = request.FILES['attachment']
                update.attachment_blob_data = uploaded_file.read()
                update.attachment_blob_filename = uploaded_file.name
                update.attachment_blob_size = uploaded_file.size
                update.attachment_blob_content_type = uploaded_file.content_type

            update.save()
            return redirect('hr_incident_detail', model_id=model_id)

    # If GET or form invalid, redirect back to detail page
    return redirect('hr_incident_detail', model_id=model_id)
