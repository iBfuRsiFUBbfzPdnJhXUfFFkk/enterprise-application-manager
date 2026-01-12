from django.db import models
from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName

class Requirement(AbstractBaseModel, AbstractComment, AbstractName):
    applications = models.ManyToManyField(Application, blank=True, related_name="%(class)s_set")
    is_for_soc = models.BooleanField(null=True, blank=True)
    is_for_spsrd = models.BooleanField(null=True, blank=True)
    is_functional_requirement = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
