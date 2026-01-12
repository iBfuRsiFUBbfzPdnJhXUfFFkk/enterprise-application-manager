from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from gitlab_sync.models.common.abstract import AbstractGitLabWebUrl


class GitLabSyncBranch(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a Git branch synced from GitLab EE 17.11.6.

    New entity for tracking branches and their status.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="branches",
    )
    repository = models.ForeignKey(
        "gitlab_sync.GitLabSyncRepository",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="branches",
    )
    commit_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_short_id: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_title: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_message: str | None = models.CharField(max_length=255, null=True, blank=True)
    merged: bool | None = models.BooleanField(null=True, blank=True)
    protected: bool | None = models.BooleanField(null=True, blank=True)
    default: bool | None = models.BooleanField(null=True, blank=True)
    developers_can_push: bool | None = models.BooleanField(null=True, blank=True)
    developers_can_merge: bool | None = models.BooleanField(null=True, blank=True)
    can_push: bool | None = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["-default", "name"]
        verbose_name = "GitLab Sync Branch"
        verbose_name_plural = "GitLab Sync Branches"
