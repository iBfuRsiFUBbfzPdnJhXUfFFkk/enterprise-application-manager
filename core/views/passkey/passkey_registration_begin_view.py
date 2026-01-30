import secrets
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from webauthn import generate_registration_options
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
)
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url

from core.models.passkey_challenge import CHALLENGE_TYPE_REGISTRATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey
from core.utilities.webauthn import get_webauthn_rp_id


@login_required
@require_http_methods(['POST'])
def passkey_registration_begin_view(request: HttpRequest) -> JsonResponse:
    """
    Begin WebAuthn passkey registration for authenticated user.
    Generates registration options and creates a challenge.
    """
    try:
        data = json.loads(request.body)
        passkey_name = data.get('name', 'Unnamed Passkey')

        # Ensure session is created
        if not request.session.session_key:
            request.session.create()

        # Get dynamic RP_ID based on current hostname
        rp_id = get_webauthn_rp_id(request)

        # Get list of existing credentials to exclude (only for current RP_ID)
        existing_passkeys = UserPasskey.objects.filter(user=request.user, rp_id=rp_id)
        exclude_credentials = [
            {'id': base64url_to_bytes(passkey.credential_id), 'type': 'public-key'}
            for passkey in existing_passkeys
        ]

        # Generate registration options
        options = generate_registration_options(
            rp_id=rp_id,
            rp_name=settings.WEBAUTHN_RP_NAME,
            user_id=str(request.user.id).encode('utf-8'),
            user_name=request.user.username,
            user_display_name=request.user.get_full_name() or request.user.username,
            exclude_credentials=exclude_credentials,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=settings.WEBAUTHN_AUTHENTICATOR_ATTACHMENT,
                resident_key=settings.WEBAUTHN_RESIDENT_KEY,
                user_verification=UserVerificationRequirement(settings.WEBAUTHN_USER_VERIFICATION),
            ),
            attestation=settings.WEBAUTHN_ATTESTATION,
        )

        # Store challenge in database (as base64url string)
        challenge_b64 = bytes_to_base64url(options.challenge)
        challenge = PasskeyChallenge.objects.create(
            challenge_type=CHALLENGE_TYPE_REGISTRATION,
            challenge=challenge_b64,
            user=request.user,
            session_key=request.session.session_key,
        )

        # Convert options to JSON-serializable format
        options_json = {
            'challenge': challenge_b64,
            'rp': {'name': options.rp.name, 'id': options.rp.id},
            'user': {
                'id': bytes_to_base64url(options.user.id),
                'name': options.user.name,
                'displayName': options.user.display_name,
            },
            'pubKeyCredParams': [
                {'type': param.type, 'alg': param.alg} for param in options.pub_key_cred_params
            ],
            'timeout': options.timeout,
            'excludeCredentials': [
                {'id': bytes_to_base64url(cred.id), 'type': cred.type, 'transports': cred.transports or []}
                for cred in (options.exclude_credentials or [])
            ],
            'authenticatorSelection': {
                'authenticatorAttachment': options.authenticator_selection.authenticator_attachment,
                'residentKey': options.authenticator_selection.resident_key,
                'userVerification': options.authenticator_selection.user_verification,
            },
            'attestation': options.attestation,
        }

        return JsonResponse({'success': True, 'options': options_json, 'challenge_id': str(challenge.uuid)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
