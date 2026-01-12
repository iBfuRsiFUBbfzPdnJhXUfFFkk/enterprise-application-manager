from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class API(AbstractBaseModel, AbstractComment, AbstractName):
    url_local = models.CharField(max_length=255, null=True, blank=True)
    url_development = models.CharField(max_length=255, null=True, blank=True)
    url_staging = models.CharField(max_length=255, null=True, blank=True)
    url_production = models.CharField(max_length=255, null=True, blank=True)
    url_production_external = models.CharField(max_length=255, null=True, blank=True)
    url_documentation = models.CharField(max_length=255, null=True, blank=True)

    service_provider = models.ForeignKey(
        'ServiceProvider',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apis'
    )
    tool = models.ForeignKey('Tool', on_delete=models.SET_NULL, null=True, blank=True, related_name='apis')
    dependencies = models.ManyToManyField('Dependency', blank=True, related_name='apis')
    applications = models.ManyToManyField('Application', blank=True, related_name='apis')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "APIs"
        ordering = ['name', '-id']
