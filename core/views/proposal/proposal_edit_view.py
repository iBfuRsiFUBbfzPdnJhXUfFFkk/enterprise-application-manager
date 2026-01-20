from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.proposal_form import ProposalForm
from core.models.proposal import Proposal
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def proposal_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        proposal = Proposal.objects.get(id=model_id)
    except Proposal.DoesNotExist:
        return generic_500(request=request)

    if request.method == "POST":
        form = ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect(to="proposal")
    else:
        form = ProposalForm(instance=proposal)

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
        template_name="authenticated/proposal/proposal_form.html",
    )
