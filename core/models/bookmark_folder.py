from django.conf import settings
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName


class BookmarkFolder(AbstractBaseModel, AbstractName):
    """
    Represents a personal bookmark folder for organizing links.
    Supports unlimited nesting via self-referencing foreign key.
    Each user has their own independent folder structure.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookmark_folders',
    )

    parent_folder = models.ForeignKey(
        'core.BookmarkFolder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_folders',
    )

    order = models.IntegerField(null=True, blank=True)

    color: str | None = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text='Hex color code (e.g., #3B82F6)',
    )

    def __str__(self):
        return f"{self.user.username}: {self.name}"

    class Meta:
        ordering = ['order', 'name', 'id']
        unique_together = [['user', 'name', 'parent_folder']]

    @property
    def get_breadcrumb(self) -> list['BookmarkFolder']:
        """
        Returns list of folders from root to this folder.
        Example: [Root, Subfolder1, Subfolder2, Current]
        """
        breadcrumb = [self]
        current = self.parent_folder
        while current:
            breadcrumb.insert(0, current)
            current = current.parent_folder
        return breadcrumb

    @property
    def get_depth(self) -> int:
        """Returns the depth level of this folder (0 = root)."""
        depth = 0
        current = self.parent_folder
        while current:
            depth += 1
            current = current.parent_folder
        return depth

    @property
    def get_all_children_recursive(self) -> list['BookmarkFolder']:
        """
        Returns all descendant folders recursively.
        Useful for operations that need to act on entire subtree.
        """
        children = []
        for child in self.child_folders.all():
            children.append(child)
            children.extend(child.get_all_children_recursive)
        return children

    @property
    def get_total_bookmark_count(self) -> int:
        """Returns total bookmarks in this folder and all subfolders."""
        count = self.bookmarks.count()
        for child in self.child_folders.all():
            count += child.get_total_bookmark_count
        return count
