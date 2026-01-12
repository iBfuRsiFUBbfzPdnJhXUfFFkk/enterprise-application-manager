from django.db import models


class AbstractGitLabTaskCompletionStatus(models.Model):
    task_completion_status_completed_count: int | None = models.IntegerField(null=True, blank=True)
    task_completion_status_count: int | None = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
