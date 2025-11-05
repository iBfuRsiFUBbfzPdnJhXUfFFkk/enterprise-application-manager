from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncPipeline(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    """
    Represents a CI/CD pipeline run synced from GitLab EE 17.11.6.

    New entity for tracking pipeline executions and build status.
    """

    project = create_generic_fk(
        related_name="pipelines",
        to="gitlab_sync.GitLabSyncProject",
    )
    merge_request = create_generic_fk(
        related_name="pipelines",
        to="gitlab_sync.GitLabSyncMergeRequest",
    )
    user = create_generic_fk(
        related_name="pipelines_triggered",
        to="gitlab_sync.GitLabSyncUser",
    )
    sha: str | None = create_generic_varchar()
    ref: str | None = create_generic_varchar()
    status: str | None = create_generic_varchar()
    source: str | None = create_generic_varchar()
    started_at: datetime | None = create_generic_datetime()
    finished_at: datetime | None = create_generic_datetime()
    duration = create_generic_decimal()
    queued_duration = create_generic_decimal()
    coverage: str | None = create_generic_varchar()
    name: str | None = create_generic_varchar()
    yaml_errors: str | None = create_generic_varchar()
    last_synced_at: datetime | None = create_generic_datetime()

    @property
    def jobs(self):
        from gitlab_sync.models.gitlab_sync_job import GitLabSyncJob

        return cast_query_set(
            typ=GitLabSyncJob, val=GitLabSyncJob.objects.filter(pipeline=self)
        )

    def __str__(self) -> str:
        return f"Pipeline #{self.id} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Pipeline"
        verbose_name_plural = "GitLab Sync Pipelines"
