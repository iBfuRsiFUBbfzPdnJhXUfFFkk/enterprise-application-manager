from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName


class GitLabSyncTag(
    AbstractBaseModel,
    AbstractName,
):
    """
    Represents a Git tag (version release) synced from GitLab EE 17.11.6.

    New entity for tracking releases and version tags.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tags",
    )
    repository = models.ForeignKey(
        "gitlab_sync.GitLabSyncRepository",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tags",
    )
    commit_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_short_id: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_title: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_message: str | None = models.CharField(max_length=255, null=True, blank=True)
    commit_created_at: datetime | None = models.DateTimeField(null=True, blank=True)
    message: str | None = models.CharField(max_length=255, null=True, blank=True)
    release_description: str | None = models.CharField(max_length=255, null=True, blank=True)
    protected: bool | None = models.BooleanField(null=True, blank=True)
    target: str | None = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["-commit_created_at"]
        verbose_name = "GitLab Sync Tag"
        verbose_name_plural = "GitLab Sync Tags"
