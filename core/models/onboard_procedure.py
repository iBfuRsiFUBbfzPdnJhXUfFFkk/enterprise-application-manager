from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.tool import Tool


class OnboardProcedure(BaseModel, Comment, Name):
    tools = create_generic_m2m(to=Tool)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
