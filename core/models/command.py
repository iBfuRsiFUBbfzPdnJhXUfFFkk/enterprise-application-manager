from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Command(AbstractBaseModel, AbstractComment, AbstractName):
    command = create_generic_varchar()

    def __str__(self):
        return f"{self.name} {self.command}"

    class Meta:
        ordering = ['name', '-id']
