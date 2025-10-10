from django.http import HttpRequest, HttpResponse

from core.forms.client_form import ClientForm
from core.models.client import Client
from core.utilities.get_user_from_request import get_user_from_request
from core.utilities.wrap_with_global_context import wrap_with_global_context
from core.views.generic.generic_500 import generic_500


def client_add_view(request: HttpRequest) -> HttpResponse:
    """
    Create a new client.
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            model: Client = form.save(commit=False)
            user = get_user_from_request(request)
            model._history_user = user
            model.save()
            return wrap_with_global_context(
                context={'models': Client.objects.all()},
                request=request,
                template='authenticated/client/client.html',
            )
        else:
            return generic_500(request, exception=Exception(form.errors))

    form = ClientForm()

    return wrap_with_global_context(
        context={'form': form},
        request=request,
        template='authenticated/client/client_form.html',
    )
