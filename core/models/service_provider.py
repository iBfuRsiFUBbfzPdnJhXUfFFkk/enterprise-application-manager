from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from core.models.tool import Tool


class ServiceProvider(AbstractBaseModel, AbstractComment, AbstractName, AbstractUniformResourceLocator):
    tools = models.ManyToManyField(
        Tool,
        blank=True,
        related_name='service_providers'
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
