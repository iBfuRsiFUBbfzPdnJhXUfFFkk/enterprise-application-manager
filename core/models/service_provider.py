from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.url import UniformResourceLocator


class ServiceProvider(BaseModel, Comment, Name, UniformResourceLocator):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
