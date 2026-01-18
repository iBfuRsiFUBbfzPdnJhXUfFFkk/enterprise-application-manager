import json
import logging

from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.models.comment import Comment

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def comment_create_ajax_view(request: HttpRequest) -> JsonResponse:
    """Create a new comment via AJAX and return rendered HTML."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    content_type_id = data.get('content_type')
    object_id = data.get('object_id')
    content = data.get('content', '').strip()
    is_internal = data.get('is_internal', False)

    if not content:
        return JsonResponse({'error': 'Content is required'}, status=400)

    if not content_type_id or not object_id:
        return JsonResponse({'error': 'Invalid target object'}, status=400)

    try:
        content_type = ContentType.objects.get(id=content_type_id)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    # Verify the target object exists
    model_class = content_type.model_class()
    if not model_class.objects.filter(id=object_id).exists():
        return JsonResponse({'error': 'Target object not found'}, status=404)

    # Non-staff users cannot create internal comments
    if is_internal and not request.user.is_staff:
        is_internal = False

    comment = Comment.objects.create(
        content_type=content_type,
        object_id=object_id,
        content=content,
        is_internal=is_internal,
        created_by=request.user,
    )

    html = render_to_string(
        'authenticated/common/components/comment_item.html',
        {'comment': comment, 'user': request.user},
        request=request,
    )

    return JsonResponse({
        'success': True,
        'comment_id': comment.id,
        'html': html,
    })
