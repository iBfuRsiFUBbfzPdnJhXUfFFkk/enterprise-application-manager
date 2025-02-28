from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name


class Incident(BaseModel, Comment, Name):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
