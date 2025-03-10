from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_m2m import create_generic_m2m


class Requirement(AbstractBaseModel, AbstractComment, AbstractName):
    applications = create_generic_m2m(to=Application)
    is_for_soc = create_generic_boolean()
    is_for_spsrd = create_generic_boolean()
    is_functional_requirement = create_generic_boolean()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
