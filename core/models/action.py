from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.url import UniformResourceLocator
from core.models.common.field_factories.create_generic_integer import create_generic_integer


class Action(BaseModel, Comment, Name, UniformResourceLocator):
    estimated_run_time_in_seconds = create_generic_integer()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
