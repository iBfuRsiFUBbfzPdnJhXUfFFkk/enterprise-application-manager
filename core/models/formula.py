from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Formula(AbstractBaseModel, AbstractComment, AbstractName):
    formula = create_generic_varchar()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
