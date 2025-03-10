from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.programing_concept_choices import PROGRAMING_CONCEPT_CHOICES
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_m2m import create_generic_m2m


class Dependency(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    applications = create_generic_m2m(to=Application)
    is_heavy = create_generic_boolean()
    type_programing_concept = create_generic_enum(choices=PROGRAMING_CONCEPT_CHOICES)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        verbose_name_plural = "Dependencies"
        ordering = ['name', 'type_programing_concept', 'version', '-id']
