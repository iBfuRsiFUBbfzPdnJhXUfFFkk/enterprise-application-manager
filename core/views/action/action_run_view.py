from datetime import datetime, UTC
from time import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from requests import get, Response

from core.models.action import Action
from core.models.user import User
from core.utilities.base_render import base_render


def action_run_view(request: HttpRequest, model_id: int) -> HttpResponse:
    start_time: float = time()
    user: AbstractBaseUser | AnonymousUser = request.user
    user_id: int = user.id
    user_instance: User | None = User.objects.filter(id=user_id).first()
    action: Action = get_object_or_404(Action, id=model_id)
    response: Response = get(cookies=request.COOKIES, timeout=180, url=action.url)
    response.raise_for_status()
    action.number_of_times_run = (action.number_of_times_run or 0) + 1
    action.user_of_last_run = user_instance
    action.datetime_of_last_run = datetime.now(tz=UTC)
    action.save()
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    action.estimated_run_time_in_seconds = int(execution_time_in_seconds)
    action.save()
    return base_render(
        context={
            "action_url": action.url,
            "execution_time_in_seconds": execution_time_in_seconds,
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
