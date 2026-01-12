from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from gitlab_sync.models.common.abstract import AbstractGitLabWebUrl


class GitLabSyncSnippet(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a code snippet synced from GitLab EE 17.11.6.

    Snippets are small pieces of code or text stored in GitLab.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="snippets",
    )
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="snippets",
    )
    gitlab_id: int | None = models.IntegerField(null=True, blank=True)
    title: str | None = models.CharField(max_length=255, null=True, blank=True)
    file_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    description: str | None = models.CharField(max_length=255, null=True, blank=True)
    visibility: str | None = models.CharField(
        max_length=255,
        choices=[
            ("private", "Private"),
            ("internal", "Internal"),
            ("public", "Public"),
        ],
        null=True,
        blank=True,
    )
    raw_url: str | None = models.CharField(max_length=255, null=True, blank=True)
    created_at: datetime | None = models.DateTimeField(null=True, blank=True)
    updated_at: datetime | None = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "GitLab Sync Snippet"
        verbose_name_plural = "GitLab Sync Snippets"
