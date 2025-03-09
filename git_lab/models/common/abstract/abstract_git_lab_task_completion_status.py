from django.db.models import Model

from core.models.common.field_factories.create_generic_integer import create_generic_integer


class AbstractGitLabTaskCompletionStatus(Model):
    task_completion_status_completed_count: int | None = create_generic_integer()
    task_completion_status_count: int | None = create_generic_integer()

    class Meta:
        abstract = True
