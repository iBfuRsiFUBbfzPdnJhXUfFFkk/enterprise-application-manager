from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.competitor_form import CompetitorForm
from core.models.competitor import Competitor
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def competitor_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        competitor = Competitor.objects.get(id=model_id)
    except Competitor.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = CompetitorForm(request.POST, instance=competitor)
        if form.is_valid():
            form.save()
            return redirect('competitor')
    else:
        form = CompetitorForm(instance=competitor)

    return base_render(
        request=request,
        template_name='authenticated/competitor/competitor_form.html',
        context={'form': form}
    )
