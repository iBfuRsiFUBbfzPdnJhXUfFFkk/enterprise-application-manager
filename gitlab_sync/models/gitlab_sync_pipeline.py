from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
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

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pipelines",
    )
    merge_request = models.ForeignKey(
        "gitlab_sync.GitLabSyncMergeRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pipelines",
    )
    user = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pipelines_triggered",
    )
    sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    ref: str | None = models.CharField(max_length=255, null=True, blank=True)
    status: str | None = models.CharField(max_length=255, null=True, blank=True)
    source: str | None = models.CharField(max_length=255, null=True, blank=True)
    started_at: datetime | None = models.DateTimeField(null=True, blank=True)
    finished_at: datetime | None = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    queued_duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    coverage: str | None = models.CharField(max_length=255, null=True, blank=True)
    name: str | None = models.CharField(max_length=255, null=True, blank=True)
    yaml_errors: str | None = models.CharField(max_length=255, null=True, blank=True)
    last_synced_at: datetime | None = models.DateTimeField(null=True, blank=True)

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
