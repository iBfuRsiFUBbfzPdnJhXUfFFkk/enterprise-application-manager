from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.url import UniformResourceLocator
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.user import User


class Action(BaseModel, Comment, Name, UniformResourceLocator):
    datetime_of_last_run = create_generic_datetime()
    estimated_run_time_in_seconds = create_generic_integer()
    number_of_times_run = create_generic_integer()
    user_of_last_run = create_generic_fk(to=User)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
