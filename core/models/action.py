from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from django.db import models
from core.models.user import User


class Action(AbstractBaseModel, AbstractComment, AbstractName, AbstractUniformResourceLocator):
    datetime_of_last_run = models.DateTimeField(null=True, blank=True)
    estimated_run_time_in_seconds = models.IntegerField(null=True, blank=True)
    number_of_times_run = models.IntegerField(null=True, blank=True)
    user_of_last_run = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_last_run')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
