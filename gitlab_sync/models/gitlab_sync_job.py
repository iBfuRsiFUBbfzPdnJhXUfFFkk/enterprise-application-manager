from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
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

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    pipeline = models.ForeignKey(
        "gitlab_sync.GitLabSyncPipeline",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs",
    )
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs",
    )
    user = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs_triggered",
    )
    stage: str | None = models.CharField(max_length=255, null=True, blank=True)
    status: str | None = models.CharField(max_length=255, null=True, blank=True)
    ref: str | None = models.CharField(max_length=255, null=True, blank=True)
    tag: bool | None = models.BooleanField(null=True, blank=True)
    coverage: str | None = models.CharField(max_length=255, null=True, blank=True)
    allow_failure: bool | None = models.BooleanField(null=True, blank=True)
    started_at: datetime | None = models.DateTimeField(null=True, blank=True)
    finished_at: datetime | None = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    queued_duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    failure_reason: str | None = models.CharField(max_length=255, null=True, blank=True)
    runner_description: str | None = models.CharField(max_length=255, null=True, blank=True)

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
