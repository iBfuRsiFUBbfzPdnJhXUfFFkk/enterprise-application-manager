from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.project import Project


class BillingCode(AbstractBaseModel, AbstractComment, AbstractName):
    application = create_generic_fk(to=Application)
    application_group = create_generic_fk(to=ApplicationGroup)
    billing_code = create_generic_varchar()
    project = create_generic_fk(to=Project)

    def __str__(self):
        return f"{self.name} - {self.billing_code}"

    class Meta:
        ordering = ['-id']
