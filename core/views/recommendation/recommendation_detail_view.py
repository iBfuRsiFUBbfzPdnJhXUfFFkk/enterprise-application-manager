from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from markdown import markdown

from core.models.recommendation import Recommendation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def recommendation_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Display detailed view of a recommendation with rendered markdown."""
    try:
        recommendation = Recommendation.objects.select_related(
            "application",
            "project",
            "estimation",
            "person_recommended_by",
        ).get(id=model_id)
    except Recommendation.DoesNotExist:
        return generic_500(request=request)

    # Render markdown fields to HTML
    description_html = markdown(recommendation.description or "") if recommendation.description else ""
    rationale_html = markdown(recommendation.rationale or "") if recommendation.rationale else ""
    benefits_html = markdown(recommendation.benefits or "") if recommendation.benefits else ""
    risks_html = markdown(recommendation.risks or "") if recommendation.risks else ""
    comment_html = markdown(recommendation.comment or "") if recommendation.comment else ""

    context: Mapping[str, Any] = {
        "recommendation": recommendation,
        "description_html": description_html,
        "rationale_html": rationale_html,
        "benefits_html": benefits_html,
        "risks_html": risks_html,
        "comment_html": comment_html,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/recommendation/recommendation_detail.html",
    )
