from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.models.person import Person


class Project(AbstractBaseModel, AbstractComment, AbstractName):
    applications = create_generic_m2m(to=Application)
    code_billing = create_generic_varchar()
    person_stake_holders = create_generic_m2m(to=Person)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
