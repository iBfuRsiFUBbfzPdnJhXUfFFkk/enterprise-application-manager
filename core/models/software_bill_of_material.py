from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class SoftwareBillOfMaterial(AbstractBaseModel, AbstractComment, AbstractName):
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
