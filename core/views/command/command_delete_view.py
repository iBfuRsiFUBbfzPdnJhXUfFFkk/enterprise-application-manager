from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.command import Command
from core.views.generic.generic_500 import generic_500


def command_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        command = Command.objects.get(id=model_id)
        command.delete()
    except Command.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='command')
