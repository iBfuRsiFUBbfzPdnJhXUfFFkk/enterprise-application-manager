from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from core.models.release import Release


def release_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    model: Release = get_object_or_404(klass=Release, pk=model_id)
    return render(context={"model": model}, request=request, template_name='release/release_detail.html')
