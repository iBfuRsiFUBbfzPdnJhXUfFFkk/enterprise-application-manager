from core.models.common.abstract.acronym import Acronym
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name


class Policy(Acronym, Comment, Name):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name_plural = "policies"
