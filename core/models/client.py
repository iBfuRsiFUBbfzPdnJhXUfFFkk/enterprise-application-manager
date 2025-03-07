from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from core.utilities.get_name_acronym import get_name_acronym


class Client(AbstractAcronym, AbstractBaseModel, AbstractComment, AbstractLocation, AbstractName, AbstractUniformResourceLocator):
    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
