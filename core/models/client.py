from core.models.common.abstract.comment import Comment
from core.models.common.abstract.location import Location
from core.models.common.abstract.name import Name
from core.models.common.abstract.url import UniformResourceLocator


class Client(Comment, Location, Name, UniformResourceLocator):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
