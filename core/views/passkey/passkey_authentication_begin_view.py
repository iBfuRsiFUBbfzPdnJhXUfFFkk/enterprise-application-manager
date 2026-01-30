import secrets

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from webauthn import generate_authentication_options
from webauthn.helpers.structs import UserVerificationRequirement
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url

from core.models.passkey_challenge import CHALLENGE_TYPE_AUTHENTICATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey
from core.utilities.webauthn import get_webauthn_rp_id


@require_http_methods(['POST'])
def passkey_authentication_begin_view(request: HttpRequest) -> JsonResponse:
    """
    Begin WebAuthn passkey authentication (passwordless login).
    Generates authentication options and creates a challenge.

    Only returns passkeys that match the current RP_ID, since passkeys
    registered on different domains won't work due to WebAuthn spec constraints.
    """
    try:
        # Ensure session is created
        if not request.session.session_key:
            request.session.create()

        # Get dynamic RP_ID based on current hostname
        rp_id = get_webauthn_rp_id(request)

        # Only get passkeys registered on this domain (they won't work cross-domain)
        matching_passkeys = UserPasskey.objects.filter(rp_id=rp_id)
        allow_credentials = [
            {'id': base64url_to_bytes(passkey.credential_id), 'type': 'public-key', 'transports': []}
            for passkey in matching_passkeys
        ]

        # Generate authentication options
        options = generate_authentication_options(
            rp_id=rp_id,
            allow_credentials=allow_credentials if allow_credentials else None,
            user_verification=UserVerificationRequirement(settings.WEBAUTHN_USER_VERIFICATION),
        )

        # Store challenge in database (no user association for passwordless flow)
        challenge_b64 = bytes_to_base64url(options.challenge)
        challenge = PasskeyChallenge.objects.create(
            challenge_type=CHALLENGE_TYPE_AUTHENTICATION,
            challenge=challenge_b64,
            user=None,  # Passwordless - user determined after authentication
            session_key=request.session.session_key,
        )

        # Convert options to JSON-serializable format
        # Note: options.allow_credentials might be objects or dicts depending on webauthn version
        allow_creds_json = []
        if options.allow_credentials:
            for cred in options.allow_credentials:
                if isinstance(cred, dict):
                    # Already a dict, just convert the id to base64url if needed
                    cred_id = cred['id']
                    if isinstance(cred_id, bytes):
                        cred_id = bytes_to_base64url(cred_id)
                    allow_creds_json.append({
                        'id': cred_id,
                        'type': cred.get('type', 'public-key'),
                        'transports': cred.get('transports', []),
                    })
                else:
                    # It's an object with attributes
                    allow_creds_json.append({
                        'id': bytes_to_base64url(cred.id),
                        'type': cred.type,
                        'transports': cred.transports or [],
                    })

        options_json = {
            'challenge': challenge_b64,
            'timeout': options.timeout,
            'rpId': options.rp_id,
            'allowCredentials': allow_creds_json,
            'userVerification': options.user_verification,
        }

        return JsonResponse({'success': True, 'options': options_json, 'challenge_id': str(challenge.uuid)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
