from django.db import models

from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.user import User


class ApplicationPin(AbstractBaseModel):
    """
    User-specific pinned applications with custom ordering.

    Allows users to pin applications to the top of their application list
    and reorder them via drag-and-drop functionality.
    """

    _disable_history = True  # User preference/UI state - low business value for audit trail

    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pins',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pinned_applications',
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order (lower numbers appear first)',
    )

    class Meta:
        ordering = ['user', 'order', 'id']
        unique_together = [['user', 'application']]
        indexes = [
            models.Index(fields=['user', 'order']),
            models.Index(fields=['user', 'application']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.application} (order: {self.order})"
