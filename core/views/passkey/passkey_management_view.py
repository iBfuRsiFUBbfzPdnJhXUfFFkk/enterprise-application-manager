from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models.user_passkey import UserPasskey
from core.utilities.webauthn import get_webauthn_rp_id


@login_required
def passkey_management_view(request: HttpRequest) -> HttpResponse:
    """
    Display list of user's registered passkeys.
    Allows users to manage their passkeys (view, rename, delete).
    Shows which domain each passkey was registered on.
    """
    current_rp_id = get_webauthn_rp_id(request)
    passkeys = UserPasskey.objects.filter(user=request.user).order_by('-created_at')

    # Check if user has any passkeys for the current domain
    has_passkey_for_current_domain = passkeys.filter(rp_id=current_rp_id).exists()

    context = {
        'passkeys': passkeys,
        'current_rp_id': current_rp_id,
        'has_passkey_for_current_domain': has_passkey_for_current_domain,
    }

    return render(request, 'authenticated/passkey/passkey_management.html', context)
