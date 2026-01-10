import base64
import json

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from webauthn import verify_authentication_response
from webauthn.helpers.structs import AuthenticationCredential

from core.models.passkey_challenge import CHALLENGE_TYPE_AUTHENTICATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey


@require_http_methods(['POST'])
def passkey_authentication_complete_view(request: HttpRequest) -> JsonResponse:
    """
    Complete WebAuthn passkey authentication (passwordless login).
    Verifies the authentication response and logs in the user.
    """
    try:
        data = json.loads(request.body)

        # Parse credential from request
        credential_id = data['id']
        raw_id = data['rawId']
        response_data = data['response']

        # Find passkey by credential ID
        credential_id_b64 = base64.b64encode(base64.urlsafe_b64decode(raw_id + '==')).decode('utf-8')

        try:
            passkey = UserPasskey.objects.select_related('user').get(credential_id=credential_id_b64)
        except UserPasskey.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Passkey not found'}, status=404)

        # Parse challenge from client data
        client_data_b64 = base64.urlsafe_b64decode(response_data['clientDataJSON'] + '==')
        client_data_json = json.loads(client_data_b64)
        challenge_str = client_data_json['challenge']

        # Get challenge from database
        try:
            challenge = PasskeyChallenge.objects.get(
                challenge=challenge_str,
                challenge_type=CHALLENGE_TYPE_AUTHENTICATION,
                used=False,
            )
        except PasskeyChallenge.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid or expired challenge'}, status=400)

        if not challenge.is_valid():
            return JsonResponse({'success': False, 'error': 'Challenge has expired'}, status=400)

        # Create AuthenticationCredential object for verification
        credential = AuthenticationCredential(
            id=credential_id,
            raw_id=base64.urlsafe_b64decode(raw_id + '=='),
            response={
                'client_data_json': base64.urlsafe_b64decode(response_data['clientDataJSON'] + '=='),
                'authenticator_data': base64.urlsafe_b64decode(response_data['authenticatorData'] + '=='),
                'signature': base64.urlsafe_b64decode(response_data['signature'] + '=='),
                'user_handle': (
                    base64.urlsafe_b64decode(response_data['userHandle'] + '==')
                    if response_data.get('userHandle')
                    else None
                ),
            },
            type=data['type'],
        )

        # Verify the authentication response
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=challenge.challenge.encode('utf-8'),
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
            credential_public_key=base64.b64decode(passkey.public_key),
            credential_current_sign_count=passkey.sign_count,
        )

        # Update passkey sign count and last used timestamp
        passkey.sign_count = verification.new_sign_count
        passkey.last_used_at = timezone.now()
        passkey.save(update_fields=['sign_count', 'last_used_at'])

        # Mark challenge as used
        challenge.used = True
        challenge.save(update_fields=['used'])

        # Log in the user using Django's login function
        login(request, passkey.user, backend='core.backends.passkey_backend.PasskeyBackend')

        # Session expires when browser closes (same as password login)
        request.session.set_expiry(0)

        return JsonResponse(
            {'success': True, 'redirect_url': '/authenticated/home/', 'username': passkey.user.username}
        )

    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
