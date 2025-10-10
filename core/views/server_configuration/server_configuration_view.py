from typing import Mapping, Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.this_server_configuration_form import ThisServerConfigurationForm
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


@login_required
def server_configuration_view(request: HttpRequest) -> HttpResponse:
    """
    Display and edit the server configuration.
    Only accessible to superusers.
    """
    # Check if user is superuser
    if not request.user.is_superuser:
        return generic_500(request=request)

    # Get or create the configuration (there should only be one)
    config = ThisServerConfiguration.current()

    # If config doesn't have a pk, it's the default - need to save it first
    if not config.pk:
        config.save()

    if request.method == 'POST':
        form = ThisServerConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect(to='server_configuration')
    else:
        form = ThisServerConfigurationForm(instance=config)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/server_configuration/server_configuration_form.html'
    )
