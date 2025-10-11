from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.requirement_form import RequirementForm
from core.models.requirement import Requirement
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def requirement_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        requirement = Requirement.objects.get(id=model_id)
    except Requirement.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = RequirementForm(request.POST, instance=requirement)
        if form.is_valid():
            form.save()
            return redirect('requirement')
    else:
        form = RequirementForm(instance=requirement)

    return base_render(
        request=request,
        template_name='authenticated/requirement/requirement_form.html',
        context={'form': form}
    )
