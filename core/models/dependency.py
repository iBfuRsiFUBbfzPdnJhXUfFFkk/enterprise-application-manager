from core.models.application import Application
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.version import Version
from core.models.common.enums.dependency_choice import DEPENDENCY_TYPE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Dependency(Comment, Version):
    applications = create_generic_m2m(to=Application)
    dependency_name = create_generic_varchar()
    is_heavy = create_generic_boolean()
    type_dependency = create_generic_enum(choices=DEPENDENCY_TYPE_CHOICES)

    def __str__(self):
        return f"{self.dependency_name} v{self.version}"

    class Meta:
        verbose_name_plural = "Dependencies"
