from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.estimation import Estimation
from core.models.estimation_item import EstimationItem


@require_http_methods(["POST"])
def estimation_group_rename_view(request: HttpRequest, estimation_id: int) -> JsonResponse:
    """
    Rename a group within an estimation.
    Updates all estimation items with the old group name to use the new group name.

    POST data should contain:
    - old_group_name: Current name of the group
    - new_group_name: New name for the group
    """
    try:
        estimation = Estimation.objects.get(id=estimation_id)

        old_group_name = request.POST.get('old_group_name', '').strip()
        new_group_name = request.POST.get('new_group_name', '').strip()

        # Validation
        if not old_group_name:
            return JsonResponse({
                'success': False,
                'error': 'Old group name is required'
            }, status=400)

        if not new_group_name:
            return JsonResponse({
                'success': False,
                'error': 'New group name is required'
            }, status=400)

        if old_group_name == new_group_name:
            return JsonResponse({
                'success': False,
                'error': 'New group name must be different from old group name'
            }, status=400)

        # Check if new group name already exists (case-insensitive)
        existing_group = EstimationItem.objects.filter(
            estimation=estimation,
            group__iexact=new_group_name
        ).exclude(
            group__iexact=old_group_name
        ).first()

        if existing_group:
            return JsonResponse({
                'success': False,
                'error': f'Group name "{new_group_name}" already exists in this estimation'
            }, status=400)

        # Update all items with the old group name
        with transaction.atomic():
            items = EstimationItem.objects.filter(
                estimation=estimation,
                group__iexact=old_group_name
            )

            updated_count = items.update(group=new_group_name)

        return JsonResponse({
            'success': True,
            'message': f'Successfully renamed group from "{old_group_name}" to "{new_group_name}"',
            'updated_count': updated_count
        })

    except Estimation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Estimation not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
