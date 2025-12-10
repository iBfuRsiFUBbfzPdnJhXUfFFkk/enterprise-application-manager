from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.recommendation_form import RecommendationForm
from core.models.recommendation import Recommendation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def recommendation_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        recommendation = Recommendation.objects.get(id=model_id)
    except Recommendation.DoesNotExist:
        return generic_500(request=request)

    if request.method == "POST":
        form = RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            form.save()
            return redirect(to="recommendation")
    else:
        form = RecommendationForm(instance=recommendation)

    # Get current user's person ID if they have one
    current_user_person_id = None
    if hasattr(request.user, 'person') and request.user.person:
        current_user_person_id = request.user.person.id

    context: Mapping[str, Any] = {
        "form": form,
        "current_user_person_id": current_user_person_id,
    }
    return base_render(
        context=context,
        request=request,
        template_name="authenticated/recommendation/recommendation_form.html",
    )
