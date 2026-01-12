from django.db import models
from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.programing_concept_choices import PROGRAMING_CONCEPT_CHOICES


class Dependency(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    applications = models.ManyToManyField(Application, blank=True, related_name='dependencies')
    is_heavy = models.BooleanField(null=True, blank=True)
    type_programing_concept = models.CharField(max_length=255, choices=PROGRAMING_CONCEPT_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        verbose_name_plural = "Dependencies"
        ordering = ['name', 'type_programing_concept', 'version', '-id']
