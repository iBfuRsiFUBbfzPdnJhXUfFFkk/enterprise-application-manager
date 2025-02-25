from django.db.models import CharField, ManyToManyField, BooleanField

from core.models.application import Application
from core.models.common.comment import Comment


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

    applications = ManyToManyField(**{
        "blank": True,
        "to": Application,
    })
    dependency_name = CharField(blank=True, max_length=255, null=True)
    is_heavy = BooleanField(blank=True, default=False, null=True)
    version = CharField(blank=True, max_length=255, null=True)
    type_dependency = CharField(blank=True, choices=DEPENDENCY_TYPE_CHOICES, max_length=255, null=True)

    def __str__(self):
        return f"{self.dependency_name} v{self.version}"
