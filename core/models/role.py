from core.models.common.abstract.acronym import Acronym
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name


class Role(Acronym, Alias, Comment, Name):
    def __str__(self):
        return f"{self.name} ({self.acronym})"

    class Meta:
        ordering = ['name', '-id']
