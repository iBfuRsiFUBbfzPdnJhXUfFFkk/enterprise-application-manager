from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.models.comment import Comment


@csrf_exempt
@require_POST
def comment_delete_ajax_view(request: HttpRequest, comment_id: int) -> JsonResponse:
    """Delete a comment via AJAX. Only the author can delete their own comments."""
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)

    if comment.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    comment.delete()

    return JsonResponse({'success': True})
