from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Acronym(Comment, Name):
    acronym = create_generic_varchar()

    def __str__(self):
        return f"{self.name} ({self.acronym})"

    class Meta:
        ordering = ['name', 'acronym', '-id']
