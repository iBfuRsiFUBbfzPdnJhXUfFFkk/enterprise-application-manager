from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from markdown import markdown

from core.models.proposal import Proposal
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def proposal_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Display detailed view of a proposal with rendered markdown and updates timeline."""
    try:
        proposal = Proposal.objects.select_related(
            "person_author",
            "person_reviewer",
            "person_approver",
            "application",
            "project",
        ).prefetch_related(
            "attachments",
            "links",
            "updates__person_author",
        ).get(id=model_id)
    except Proposal.DoesNotExist:
        return generic_500(request=request)

    # Render markdown fields to HTML
    executive_summary_html = markdown(proposal.executive_summary or "") if proposal.executive_summary else ""
    problem_statement_html = markdown(proposal.problem_statement or "") if proposal.problem_statement else ""
    proposed_solution_html = markdown(proposal.proposed_solution or "") if proposal.proposed_solution else ""
    benefits_html = markdown(proposal.benefits or "") if proposal.benefits else ""
    risks_and_mitigations_html = markdown(proposal.risks_and_mitigations or "") if proposal.risks_and_mitigations else ""
    timeline_html = markdown(proposal.timeline or "") if proposal.timeline else ""
    resources_required_html = markdown(proposal.resources_required or "") if proposal.resources_required else ""
    success_criteria_html = markdown(proposal.success_criteria or "") if proposal.success_criteria else ""
    comment_html = markdown(proposal.comment or "") if proposal.comment else ""

    updates = proposal.updates.all()

    context: Mapping[str, Any] = {
        "proposal": proposal,
        "executive_summary_html": executive_summary_html,
        "problem_statement_html": problem_statement_html,
        "proposed_solution_html": proposed_solution_html,
        "benefits_html": benefits_html,
        "risks_and_mitigations_html": risks_and_mitigations_html,
        "timeline_html": timeline_html,
        "resources_required_html": resources_required_html,
        "success_criteria_html": success_criteria_html,
        "comment_html": comment_html,
        "updates": updates,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/proposal/proposal_detail.html",
    )
