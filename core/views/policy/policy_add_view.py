from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.policy_form import PolicyForm
from core.utilities.base_render import base_render


def policy_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('policy')
    else:
        form = PolicyForm()

    return base_render(
        request=request,
        template_name='authenticated/policy/policy_form.html',
        context={'form': form}
    )
