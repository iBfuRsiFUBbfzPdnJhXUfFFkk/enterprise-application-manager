from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from core.models.comment import Comment


def get_comments_context(instance: Model, user: AbstractUser) -> dict[str, Any]:
    """
    Get comments context for a model instance to use in templates.

    Args:
        instance: The model instance to get comments for
        user: The current user (to filter internal comments)

    Returns:
        Dict with 'comments', 'content_type', and 'object_id' keys
    """
    content_type = ContentType.objects.get_for_model(instance)

    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=instance.pk,
    )

    # Non-staff users can only see non-internal comments
    if not user.is_staff:
        comments = comments.filter(is_internal=False)

    return {
        'comments': list(comments),
        'content_type': content_type.id,
        'object_id': instance.pk,
    }
