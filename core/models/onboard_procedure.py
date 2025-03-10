from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from core.models.tool import Tool


class OnboardProcedure(AbstractBaseModel, AbstractComment, AbstractName):
    tools = create_generic_m2m(to=Tool)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
