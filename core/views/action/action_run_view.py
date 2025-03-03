from time import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from requests import get, Response

from core.models.action import Action
from core.utilities.base_render import base_render


def action_run_view(request: HttpRequest, model_id: int) -> HttpResponse:
    start_time: float = time()
    action: Action = get_object_or_404(Action, id=model_id)
    response: Response = get(cookies=request.COOKIES, timeout=180, url=action.url)
    response.raise_for_status()
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    print(f'Execution time: {execution_time_in_seconds} seconds')
    return base_render(
        context={
            "action_url": action.url,
            "execution_time_in_seconds": execution_time_in_seconds,
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
