from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
)


class GitLabSyncJob(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a CI/CD job within a pipeline synced from GitLab EE 17.11.6.

    New entity for tracking individual build/test/deploy jobs.
    """

    pipeline = create_generic_fk(
        related_name="jobs",
        to="gitlab_sync.GitLabSyncPipeline",
    )
    project = create_generic_fk(
        related_name="jobs",
        to="gitlab_sync.GitLabSyncProject",
    )
    user = create_generic_fk(
        related_name="jobs_triggered",
        to="gitlab_sync.GitLabSyncUser",
    )
    stage: str | None = create_generic_varchar()
    status: str | None = create_generic_varchar()
    ref: str | None = create_generic_varchar()
    tag: bool | None = create_generic_boolean()
    coverage: str | None = create_generic_varchar()
    allow_failure: bool | None = create_generic_boolean()
    started_at: datetime | None = create_generic_datetime()
    finished_at: datetime | None = create_generic_datetime()
    duration = create_generic_decimal()
    queued_duration = create_generic_decimal()
    failure_reason: str | None = create_generic_varchar()
    runner_description: str | None = create_generic_varchar()

    @property
    def artifacts(self):
        from gitlab_sync.models.gitlab_sync_artifact import GitLabSyncArtifact

        return cast_query_set(
            typ=GitLabSyncArtifact, val=GitLabSyncArtifact.objects.filter(job=self)
        )

    def __str__(self) -> str:
        return f"{self.name} (#{self.id})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Job"
        verbose_name_plural = "GitLab Sync Jobs"
