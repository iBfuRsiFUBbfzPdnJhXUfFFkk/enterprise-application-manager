from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.policy_form import PolicyForm
from core.models.policy import Policy
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def policy_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        policy = Policy.objects.get(id=model_id)
    except Policy.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect('policy')
    else:
        form = PolicyForm(instance=policy)

    return base_render(
        request=request,
        template_name='authenticated/policy/policy_form.html',
        context={'form': form}
    )
