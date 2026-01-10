import secrets

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from webauthn import generate_authentication_options
from webauthn.helpers.structs import UserVerificationRequirement

from core.models.passkey_challenge import CHALLENGE_TYPE_AUTHENTICATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey


@require_http_methods(['POST'])
def passkey_authentication_begin_view(request: HttpRequest) -> JsonResponse:
    """
    Begin WebAuthn passkey authentication (passwordless login).
    Generates authentication options and creates a challenge.
    """
    try:
        # Get all registered passkeys for allow list (passwordless flow)
        all_passkeys = UserPasskey.objects.all()
        allow_credentials = [
            {'id': passkey.credential_id, 'type': 'public-key', 'transports': []}
            for passkey in all_passkeys
        ]

        # Generate authentication options
        options = generate_authentication_options(
            rp_id=settings.WEBAUTHN_RP_ID,
            allow_credentials=allow_credentials if allow_credentials else None,
            user_verification=UserVerificationRequirement(settings.WEBAUTHN_USER_VERIFICATION),
        )

        # Store challenge in database (no user association for passwordless flow)
        challenge = PasskeyChallenge.objects.create(
            challenge_type=CHALLENGE_TYPE_AUTHENTICATION,
            challenge=options.challenge.decode('utf-8'),
            user=None,  # Passwordless - user determined after authentication
            session_key=request.session.session_key,
        )

        # Convert options to JSON-serializable format
        options_json = {
            'challenge': options.challenge.decode('utf-8'),
            'timeout': options.timeout,
            'rpId': options.rp_id,
            'allowCredentials': [
                {
                    'id': cred.id.decode('utf-8') if isinstance(cred.id, bytes) else cred.id,
                    'type': cred.type,
                    'transports': cred.transports or [],
                }
                for cred in (options.allow_credentials or [])
            ],
            'userVerification': options.user_verification,
        }

        return JsonResponse({'success': True, 'options': options_json, 'challenge_id': str(challenge.uuid)})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
