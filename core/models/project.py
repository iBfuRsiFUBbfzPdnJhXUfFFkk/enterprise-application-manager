from core.models.application import Application
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.person import Person


class Project(BaseModel, Comment, Name):
    applications = create_generic_m2m(to=Application)
    code_billing = create_generic_varchar()
    person_stake_holders = create_generic_m2m(to=Person)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
