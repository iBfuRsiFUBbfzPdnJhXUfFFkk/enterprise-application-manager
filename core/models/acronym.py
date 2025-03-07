from core.models.common.abstract.abstract_acronym import AbstractAcronym as BaseAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_pronunciation import AbstractPronunciation
from core.models.common.abstract.abstract_supporting_link import AbstractSupportingLink
from core.utilities.get_name_acronym import get_name_acronym


class Acronym(AbstractAlias, BaseAcronym, AbstractBaseModel, AbstractComment, AbstractName, AbstractPronunciation, AbstractSupportingLink):
    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', 'acronym', '-id']
