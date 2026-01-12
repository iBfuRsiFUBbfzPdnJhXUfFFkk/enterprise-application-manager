from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.tool import Tool

class OnboardProcedure(AbstractBaseModel, AbstractComment, AbstractName):
    tools = models.ManyToManyField(Tool, blank=True, related_name="%(class)s_set")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
