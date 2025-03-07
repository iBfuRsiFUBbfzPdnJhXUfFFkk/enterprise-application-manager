from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_date import create_generic_date


class ReleaseBundle(AbstractBaseModel, AbstractComment, AbstractName):
    date_code_freeze = create_generic_date()
    date_demo = create_generic_date()
    date_release = create_generic_date()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
