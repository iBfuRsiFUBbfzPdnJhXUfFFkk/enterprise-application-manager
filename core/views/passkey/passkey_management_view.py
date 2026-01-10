from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models.user_passkey import UserPasskey


@login_required
def passkey_management_view(request: HttpRequest) -> HttpResponse:
    """
    Display list of user's registered passkeys.
    Allows users to manage their passkeys (view, rename, delete).
    """
    passkeys = UserPasskey.objects.filter(user=request.user).order_by('-created_at')

    context = {'passkeys': passkeys}

    return render(request, 'authenticated/passkey/passkey_management.html', context)
