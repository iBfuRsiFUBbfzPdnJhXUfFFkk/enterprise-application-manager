from core.models.common.abstract.acronym import Acronym
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.utilities.get_name_acronym import get_name_acronym


class ApplicationGroup(Alias, Acronym, BaseModel, Comment, Name):
    is_externally_facing = create_generic_boolean()
    is_platform = create_generic_boolean()
    type_lifecycle = create_generic_enum(choices=LIFECYCLE_CHOICES)

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
