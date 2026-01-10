import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.user_passkey import UserPasskey


@login_required
@require_http_methods(['POST', 'PATCH'])
def passkey_rename_view(request: HttpRequest, passkey_uuid: str) -> JsonResponse:
    """
    Rename a user's passkey.
    Only the passkey owner can rename their own passkeys.
    """
    try:
        data = json.loads(request.body)
        new_name = data.get('name', '').strip()

        if not new_name:
            return JsonResponse({'success': False, 'error': 'Passkey name cannot be empty'}, status=400)

        passkey = UserPasskey.objects.get(uuid=passkey_uuid, user=request.user)
        passkey.name = new_name
        passkey.save(update_fields=['name'])

        return JsonResponse({'success': True, 'message': f'Passkey renamed to "{new_name}"', 'name': new_name})

    except UserPasskey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Passkey not found or access denied'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
