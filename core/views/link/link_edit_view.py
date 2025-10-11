from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.link_form import LinkForm
from core.models.link import Link
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def link_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        link = Link.objects.get(id=model_id)
    except Link.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('link')
    else:
        form = LinkForm(instance=link)

    return base_render(
        request=request,
        template_name='authenticated/link/link_form.html',
        context={'form': form}
    )
