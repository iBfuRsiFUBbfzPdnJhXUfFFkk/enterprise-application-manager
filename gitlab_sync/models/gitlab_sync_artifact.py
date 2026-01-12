from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class GitLabSyncArtifact(AbstractBaseModel):
    """
    Represents a build artifact from a CI/CD job synced from GitLab EE 17.11.6.

    New entity for tracking build outputs and artifacts.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    job = models.ForeignKey(
        "gitlab_sync.GitLabSyncJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artifacts",
    )
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artifacts",
    )
    file_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    size: int | None = models.IntegerField(null=True, blank=True)
    filename: str | None = models.CharField(max_length=255, null=True, blank=True)
    file_format: str | None = models.CharField(max_length=255, null=True, blank=True)
    expire_at: datetime | None = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.filename} ({self.file_type})"

    class Meta:
        ordering = ["-id"]
        verbose_name = "GitLab Sync Artifact"
        verbose_name_plural = "GitLab Sync Artifacts"
