from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from markdown import markdown

from core.models.approval import Approval
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def approval_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Display detailed view of an approval with rendered markdown and updates timeline."""
    try:
        approval = Approval.objects.select_related(
            "person_requester",
            "application",
            "project",
        ).prefetch_related(
            "approvers",
            "documents",
            "updates__person_author",
        ).get(id=model_id)
    except Approval.DoesNotExist:
        return generic_500(request=request)

    description_html = markdown(approval.description or "") if approval.description else ""
    comment_html = markdown(approval.comment or "") if approval.comment else ""

    updates = approval.updates.all()

    context: Mapping[str, Any] = {
        "approval": approval,
        "description_html": description_html,
        "comment_html": comment_html,
        "updates": updates,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/approval/approval_detail.html",
    )
