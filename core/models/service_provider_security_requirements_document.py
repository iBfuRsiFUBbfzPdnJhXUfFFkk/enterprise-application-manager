from core.models.application import Application
from core.models.client import Client
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.requirement import Requirement


class ServiceProviderSecurityRequirementsDocument(BaseModel, Comment, Name):
    applications = create_generic_m2m(to=Application)
    clients = create_generic_m2m(to=Client)
    requirements = create_generic_m2m(to=Requirement)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
