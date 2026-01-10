from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.user_passkey import UserPasskey


@login_required
@require_http_methods(['POST', 'DELETE'])
def passkey_delete_view(request: HttpRequest, passkey_uuid: str) -> JsonResponse:
    """
    Delete a user's passkey.
    Only the passkey owner can delete their own passkeys.
    """
    try:
        passkey = UserPasskey.objects.get(uuid=passkey_uuid, user=request.user)
        passkey_name = passkey.name
        passkey.delete()

        return JsonResponse({'success': True, 'message': f'Passkey "{passkey_name}" deleted successfully'})

    except UserPasskey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Passkey not found or access denied'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
