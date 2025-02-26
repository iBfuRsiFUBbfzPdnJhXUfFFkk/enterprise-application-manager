from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name


class Organization(Comment, Name):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
