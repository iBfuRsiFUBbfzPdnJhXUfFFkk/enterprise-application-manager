from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.approval_form import ApprovalForm
from core.utilities.base_render import base_render


def approval_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="approval")
    else:
        form = ApprovalForm()

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
        template_name="authenticated/approval/approval_form.html",
    )
