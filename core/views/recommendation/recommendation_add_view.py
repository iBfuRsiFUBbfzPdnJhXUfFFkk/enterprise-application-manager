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

    context: Mapping[str, Any] = {"form": form}
    return base_render(
        context=context,
        request=request,
        template_name="authenticated/recommendation/recommendation_form.html",
    )
