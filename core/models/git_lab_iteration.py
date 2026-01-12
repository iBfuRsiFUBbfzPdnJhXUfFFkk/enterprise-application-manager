from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class GitLabIteration(AbstractBaseModel, AbstractComment, AbstractName):
    git_lab_id = models.CharField(max_length=255, null=True, blank=True)
    sprint = models.ForeignKey('Sprint', on_delete=models.SET_NULL, null=True, blank=True, related_name="git_lab_iterations")

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']
