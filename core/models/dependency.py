from core.models.application import Application
from core.models.common.comment import Comment
from core.models.common.create_generic_boolean import create_generic_boolean
from core.models.common.create_generic_enum import create_generic_enum
from core.models.common.create_generic_m2m import create_generic_m2m
from core.models.common.create_generic_varchar import create_generic_varchar


class Dependency(Comment):
    DEPENDENCY_TYPE_CHOICES_BINARY = "Binary"
    DEPENDENCY_TYPE_CHOICES_FRAMEWORK = "Framework"
    DEPENDENCY_TYPE_CHOICES_LANGUAGE = "Language"
    DEPENDENCY_TYPE_CHOICES_PACKAGE = "Package"
    DEPENDENCY_TYPE_CHOICES_PROTOCOL = "Protocol"
    DEPENDENCY_TYPE_CHOICES_STANDARD = "Standard"

    DEPENDENCY_TYPE_CHOICES = [
        (DEPENDENCY_TYPE_CHOICES_BINARY, DEPENDENCY_TYPE_CHOICES_BINARY),
        (DEPENDENCY_TYPE_CHOICES_FRAMEWORK, DEPENDENCY_TYPE_CHOICES_FRAMEWORK),
        (DEPENDENCY_TYPE_CHOICES_LANGUAGE, DEPENDENCY_TYPE_CHOICES_LANGUAGE),
        (DEPENDENCY_TYPE_CHOICES_PACKAGE, DEPENDENCY_TYPE_CHOICES_PACKAGE),
        (DEPENDENCY_TYPE_CHOICES_PROTOCOL, DEPENDENCY_TYPE_CHOICES_PROTOCOL),
        (DEPENDENCY_TYPE_CHOICES_STANDARD, DEPENDENCY_TYPE_CHOICES_STANDARD),
    ]

    applications = create_generic_m2m(to=Application)
    dependency_name = create_generic_varchar()
    is_heavy = create_generic_boolean()
    type_dependency = create_generic_enum(choices=DEPENDENCY_TYPE_CHOICES)
    version = create_generic_varchar()

    def __str__(self):
        return f"{self.dependency_name} v{self.version}"

    class Meta:
        verbose_name_plural = "Dependencies"