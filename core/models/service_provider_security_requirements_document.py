from django.db import models
from core.models.application import Application
from core.models.client import Client
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.requirement import Requirement

class ServiceProviderSecurityRequirementsDocument(AbstractBaseModel, AbstractComment, AbstractName):
    applications = models.ManyToManyField(Application, blank=True, related_name="%(class)s_set")
    clients = models.ManyToManyField(Client, blank=True, related_name="%(class)s_set")
    requirements = models.ManyToManyField(Requirement, blank=True, related_name="%(class)s_set")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
