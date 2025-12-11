from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.it_devops_request_form import ITDevOpsRequestForm
from core.utilities.base_render import base_render


def it_devops_request_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ITDevOpsRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="it_devops_request")
    else:
        form = ITDevOpsRequestForm()

    # Get current user's person ID if they have one
    current_user_person_id = None
    if hasattr(request.user, 'person_mapping') and request.user.person_mapping:
        current_user_person_id = request.user.person_mapping.id

    context: Mapping[str, Any] = {
        "form": form,
        "current_user_person_id": current_user_person_id,
    }
    return base_render(
        context=context,
        request=request,
        template_name="authenticated/it_devops_request/it_devops_request_form.html",
    )
