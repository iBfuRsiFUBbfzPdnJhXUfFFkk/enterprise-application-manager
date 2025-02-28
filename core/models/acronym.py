from core.models.common.abstract.acronym import Acronym as BaseAcronym
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.pronunciation import Pronunciation
from core.models.common.abstract.supporting_link import SupportingLink
from core.utilities.get_name_acronym import get_name_acronym


class Acronym(Alias, BaseAcronym, BaseModel, Comment, Name, Pronunciation, SupportingLink):
    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', 'acronym', '-id']
