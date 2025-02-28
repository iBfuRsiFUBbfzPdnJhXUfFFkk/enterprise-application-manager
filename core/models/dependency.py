from core.models.application import Application
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.version import Version
from core.models.common.enums.programing_concept_choices import PROGRAMING_CONCEPT_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m


class Dependency(BaseModel, Comment, Name, Version):
    applications = create_generic_m2m(to=Application)
    is_heavy = create_generic_boolean()
    type_programing_concept = create_generic_enum(choices=PROGRAMING_CONCEPT_CHOICES)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        verbose_name_plural = "Dependencies"
        ordering = ['name', 'type_programing_concept', 'version', '-id']
