import base64
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from webauthn import verify_registration_response
from webauthn.helpers.structs import RegistrationCredential

from core.models.passkey_challenge import CHALLENGE_TYPE_REGISTRATION, PasskeyChallenge
from core.models.user_passkey import UserPasskey


@login_required
@require_http_methods(['POST'])
def passkey_registration_complete_view(request: HttpRequest) -> JsonResponse:
    """
    Complete WebAuthn passkey registration.
    Verifies the registration response and creates the passkey record.
    """
    try:
        data = json.loads(request.body)
        passkey_name = data.get('name', 'Unnamed Passkey')

        # Parse credential from request
        credential_id = data['id']
        raw_id = data['rawId']
        response_data = data['response']

        # Find and validate challenge
        challenge_b64 = base64.b64decode(response_data['clientDataJSON'])
        challenge_json = json.loads(challenge_b64)
        challenge_str = challenge_json['challenge']

        # Get challenge from database
        try:
            challenge = PasskeyChallenge.objects.get(
                challenge=challenge_str,
                challenge_type=CHALLENGE_TYPE_REGISTRATION,
                user=request.user,
                used=False,
            )
        except PasskeyChallenge.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid or expired challenge'}, status=400)

        if not challenge.is_valid():
            return JsonResponse({'success': False, 'error': 'Challenge has expired'}, status=400)

        # Create RegistrationCredential object for verification
        credential = RegistrationCredential(
            id=credential_id,
            raw_id=base64.urlsafe_b64decode(raw_id + '=='),
            response={
                'client_data_json': base64.urlsafe_b64decode(response_data['clientDataJSON'] + '=='),
                'attestation_object': base64.urlsafe_b64decode(response_data['attestationObject'] + '=='),
            },
            type=data['type'],
        )

        # Verify the registration response
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=challenge.challenge.encode('utf-8'),
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
        )

        # Create UserPasskey record
        passkey = UserPasskey.objects.create(
            user=request.user,
            name=passkey_name,
            credential_id=base64.b64encode(verification.credential_id).decode('utf-8'),
            public_key=base64.b64encode(verification.credential_public_key).decode('utf-8'),
            sign_count=verification.sign_count,
            aaguid=str(verification.aaguid) if verification.aaguid else '',
            credential_type='public-key',
            transports=json.dumps(data.get('transports', [])),
            backup_eligible=verification.credential_backup_eligible,
            backup_state=verification.credential_backed_up,
            user_verified=verification.user_verified,
        )

        # Mark challenge as used
        challenge.used = True
        challenge.save(update_fields=['used'])

        return JsonResponse({'success': True, 'passkey_name': passkey.name, 'passkey_id': str(passkey.uuid)})

    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
