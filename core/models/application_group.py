from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class ApplicationGroup(Comment, Name):
    acronym = create_generic_varchar()
    is_externally_facing = create_generic_boolean()
    is_platform = create_generic_boolean()
    name_aliases = create_generic_varchar()
    type_lifecycle = create_generic_enum(choices=LIFECYCLE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.acronym})"
