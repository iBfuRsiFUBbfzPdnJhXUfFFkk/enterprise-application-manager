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

from core.models.passkey_challenge import CHALLENGE_TYPE_REGISTRATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey


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

        # Get list of existing credentials to exclude
        existing_passkeys = UserPasskey.objects.filter(user=request.user)
        exclude_credentials = [
            {'id': passkey.credential_id, 'type': 'public-key'} for passkey in existing_passkeys
        ]

        # Generate registration options
        options = generate_registration_options(
            rp_id=settings.WEBAUTHN_RP_ID,
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

        # Store challenge in database
        challenge = PasskeyChallenge.objects.create(
            challenge_type=CHALLENGE_TYPE_REGISTRATION,
            challenge=options.challenge.decode('utf-8'),
            user=request.user,
            session_key=request.session.session_key,
        )

        # Convert options to JSON-serializable format
        options_json = {
            'challenge': options.challenge.decode('utf-8'),
            'rp': {'name': options.rp.name, 'id': options.rp.id},
            'user': {
                'id': options.user.id.decode('utf-8'),
                'name': options.user.name,
                'displayName': options.user.display_name,
            },
            'pubKeyCredParams': [
                {'type': param.type, 'alg': param.alg} for param in options.pub_key_cred_params
            ],
            'timeout': options.timeout,
            'excludeCredentials': [
                {'id': cred.id.decode('utf-8'), 'type': cred.type, 'transports': cred.transports or []}
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
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
