from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.url import UniformResourceLocator


class Server(Comment, Name, UniformResourceLocator):
    def __str__(self):
        return f"{self.name} {self.url}"

    class Meta:
        ordering = ['name', '-id']
