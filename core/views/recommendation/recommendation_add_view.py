from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.recommendation_form import RecommendationForm
from core.utilities.base_render import base_render


def recommendation_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RecommendationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="recommendation")
    else:
        form = RecommendationForm()

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
