from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.person_form import PersonForm
from core.models.person import Person
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def person_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        person = Person.objects.get(id=model_id)
    except Person.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect(to='person')
    else:
        form = PersonForm(instance=person)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/person/person_form.html'
    )
