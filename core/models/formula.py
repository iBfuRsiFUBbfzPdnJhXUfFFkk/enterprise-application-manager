from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Formula(BaseModel, Comment, Name):
    formula = create_generic_varchar()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
