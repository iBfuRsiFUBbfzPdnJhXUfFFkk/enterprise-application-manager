from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_enum import create_generic_enum
from core.utilities.get_name_acronym import get_name_acronym


class ApplicationGroup(AbstractAlias, AbstractAcronym, AbstractBaseModel, AbstractComment, AbstractName):
    is_externally_facing = create_generic_boolean()
    is_platform = create_generic_boolean()
    type_lifecycle = create_generic_enum(choices=LIFECYCLE_CHOICES)

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
