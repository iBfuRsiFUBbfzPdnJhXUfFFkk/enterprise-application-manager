from core.models.common.abstract.acronym import Acronym as BaseAcronym
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.pronunciation import Pronunciation


class Acronym(BaseAcronym, Comment, Name, Pronunciation):
    def __str__(self):
        return f"{self.name} ({self.acronym})"

    class Meta:
        ordering = ['name', 'acronym', '-id']
