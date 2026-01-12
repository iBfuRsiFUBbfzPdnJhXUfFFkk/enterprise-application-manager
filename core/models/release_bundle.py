from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName

class ReleaseBundle(AbstractBaseModel, AbstractComment, AbstractName):
    date_code_freeze = models.DateField(null=True, blank=True)
    date_demo = models.DateField(null=True, blank=True)
    date_release = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
