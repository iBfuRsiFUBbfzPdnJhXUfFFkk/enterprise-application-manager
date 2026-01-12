from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from gitlab_sync.models.common.abstract import (
    AbstractGitLabCreatedAt,
    AbstractGitLabTitle,
    AbstractGitLabWebUrl,
)


class GitLabSyncCommit(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabTitle,
    AbstractGitLabWebUrl,
):
    """
    Represents a Git commit synced from GitLab EE 17.11.6.

    New entity for tracking individual commits and code changes.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    short_id: str | None = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commits_authored",
    )
    author_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    author_email: str | None = models.CharField(max_length=255, null=True, blank=True)
    authored_date: datetime | None = models.DateTimeField(null=True, blank=True)
    committer_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    committer_email: str | None = models.CharField(max_length=255, null=True, blank=True)
    committed_date: datetime | None = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commits",
    )
    repository = models.ForeignKey(
        "gitlab_sync.GitLabSyncRepository",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commits",
    )
    message: str | None = models.CharField(max_length=255, null=True, blank=True)
    parent_ids: str | None = models.CharField(max_length=255, null=True, blank=True)
    additions: int | None = models.IntegerField(null=True, blank=True)
    deletions: int | None = models.IntegerField(null=True, blank=True)
    total_changes: int | None = models.IntegerField(null=True, blank=True)

    @property
    def pipelines(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline, val=GitLabSyncPipeline.objects.filter(sha=self.sha)
        )

    def __str__(self) -> str:
        return f"{self.short_id}: {self.title}"

    class Meta:
        ordering = ["-committed_date"]
        verbose_name = "GitLab Sync Commit"
        verbose_name_plural = "GitLab Sync Commits"
