import json
from django.http import HttpRequest, JsonResponse
from core.forms.secret_form import SecretForm


def secret_quick_add_view(request: HttpRequest) -> JsonResponse:
    """AJAX endpoint for creating secrets from modals"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    form = SecretForm(request.POST)
    if form.is_valid():
        secret = form.save()
        return JsonResponse({
            'success': True,
            'secret': {
                'id': secret.id,
                'name': secret.name,
            }
        })
    else:
        errors = {field: error[0] for field, error in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)
