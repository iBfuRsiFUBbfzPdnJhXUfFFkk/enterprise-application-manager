from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_date import create_generic_date


class ReleaseBundle(BaseModel, Comment, Name):
    date_code_freeze = create_generic_date()
    date_demo = create_generic_date()
    date_release = create_generic_date()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
