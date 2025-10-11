from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.requirement_form import RequirementForm
from core.utilities.base_render import base_render


def requirement_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requirement')
    else:
        form = RequirementForm()

    return base_render(
        request=request,
        template_name='authenticated/requirement/requirement_form.html',
        context={'form': form}
    )
