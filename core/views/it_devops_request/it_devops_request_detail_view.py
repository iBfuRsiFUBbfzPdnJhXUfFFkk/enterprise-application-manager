from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from markdown import markdown

from core.models.it_devops_request import ITDevOpsRequest
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def it_devops_request_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Display detailed view of an IT/DevOps request with rendered markdown and updates timeline."""
    try:
        it_devops_request = ITDevOpsRequest.objects.select_related(
            "person_requester",
            "person_assignee",
            "person_approver",
            "application",
            "project",
        ).prefetch_related(
            "attachments",
            "updates__person_author",
        ).get(id=model_id)
    except ITDevOpsRequest.DoesNotExist:
        return generic_500(request=request)

    # Render markdown fields to HTML
    description_html = markdown(it_devops_request.description or "") if it_devops_request.description else ""
    justification_html = markdown(it_devops_request.justification or "") if it_devops_request.justification else ""
    expected_outcome_html = markdown(it_devops_request.expected_outcome or "") if it_devops_request.expected_outcome else ""
    comment_html = markdown(it_devops_request.comment or "") if it_devops_request.comment else ""

    # Get updates ordered chronologically
    updates = it_devops_request.updates.all()

    context: Mapping[str, Any] = {
        "request": it_devops_request,
        "description_html": description_html,
        "justification_html": justification_html,
        "expected_outcome_html": expected_outcome_html,
        "comment_html": comment_html,
        "updates": updates,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/it_devops_request/it_devops_request_detail.html",
    )
