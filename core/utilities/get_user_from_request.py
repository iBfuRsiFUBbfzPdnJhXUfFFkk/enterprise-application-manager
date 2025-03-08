from typing import cast

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from core.models.user import User


def get_user_from_request(request: HttpRequest) -> User | None:
    user: AbstractBaseUser | AnonymousUser = request.user
    if isinstance(user, AnonymousUser):
        return None
    return cast(
        typ=User,
        val=user
    )
