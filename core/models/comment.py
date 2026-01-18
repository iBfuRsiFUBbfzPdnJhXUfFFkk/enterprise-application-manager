from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class Comment(AbstractBaseModel):
    """
    Central comment model that can be attached to any model via GenericForeignKey.
    Supports markdown content and internal/external visibility.
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(
        help_text='Comment content (supports markdown)',
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments_created',
    )

    is_internal = models.BooleanField(
        default=False,
        help_text='Internal comments are only visible to staff',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        author = self.created_by.username if self.created_by else 'Unknown'
        return f"Comment by {author} on {self.content_type.model}"
