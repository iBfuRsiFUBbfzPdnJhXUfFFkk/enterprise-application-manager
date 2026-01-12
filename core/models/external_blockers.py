from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.organization import Organization


class ExternalBlockers(AbstractBaseModel, AbstractComment, AbstractName):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='external_blockers')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
