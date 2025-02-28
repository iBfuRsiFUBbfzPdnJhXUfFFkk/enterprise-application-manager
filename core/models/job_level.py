from core.models.common.abstract.acronym import Acronym
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.utilities.get_name_acronym import get_name_acronym


class JobLevel(BaseModel, Acronym, Comment, Name):
    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
