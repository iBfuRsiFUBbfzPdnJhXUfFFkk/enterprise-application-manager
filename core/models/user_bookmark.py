from django.conf import settings
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class UserBookmark(AbstractBaseModel):
    """
    Intermediate model linking User, Link, and optionally BookmarkFolder.
    Replaces the direct M2M relationship between User and Link.
    Allows bookmarks to be organized into folders.
    """

    _disable_history = True  # User preference/UI state - low business value for audit trail

    user = create_generic_fk(
        to=settings.AUTH_USER_MODEL,
        related_name='user_bookmarks',
    )

    link = create_generic_fk(
        to='core.Link',
        related_name='user_bookmarks',
    )

    folder = create_generic_fk(
        to='core.BookmarkFolder',
        related_name='bookmarks',
    )

    order = create_generic_integer()

    def __str__(self):
        folder_name = self.folder.name if self.folder else "Uncategorized"
        return f"{self.user.username}: {self.link.name} [{folder_name}]"

    class Meta:
        ordering = ['order', 'id']
        unique_together = [['user', 'link']]  # User can only bookmark a link once
