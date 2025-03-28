from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from core.models.user import User


class Action(AbstractBaseModel, AbstractComment, AbstractName, AbstractUniformResourceLocator):
    datetime_of_last_run = create_generic_datetime()
    estimated_run_time_in_seconds = create_generic_integer()
    number_of_times_run = create_generic_integer()
    user_of_last_run = create_generic_fk(to=User)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
