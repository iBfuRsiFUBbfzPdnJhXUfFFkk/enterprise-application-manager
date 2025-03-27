from django_generic_model_fields.create_generic_fk import create_generic_fk

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.organization import Organization


class ExternalBlockers(AbstractBaseModel, AbstractComment, AbstractName):
    organization = create_generic_fk(to=Organization)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
