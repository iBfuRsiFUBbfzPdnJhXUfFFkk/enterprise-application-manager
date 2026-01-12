from django.conf import settings
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class UserBookmark(AbstractBaseModel):
    """
    Intermediate model linking User, Link, and optionally BookmarkFolder.
    Replaces the direct M2M relationship between User and Link.
    Allows bookmarks to be organized into folders.
    """

    _disable_history = True  # User preference/UI state - low business value for audit trail

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_bookmarks',
    )

    link = models.ForeignKey(
        'core.Link',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_bookmarks',
    )

    folder = models.ForeignKey(
        'core.BookmarkFolder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookmarks',
    )

    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        folder_name = self.folder.name if self.folder else "Uncategorized"
        return f"{self.user.username}: {self.link.name} [{folder_name}]"

    class Meta:
        ordering = ['order', 'id']
        unique_together = [['user', 'link']]  # User can only bookmark a link once
