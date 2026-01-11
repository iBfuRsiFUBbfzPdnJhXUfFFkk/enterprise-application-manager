from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class GitLabSyncArtifact(AbstractBaseModel):
    """
    Represents a build artifact from a CI/CD job synced from GitLab EE 17.11.6.

    New entity for tracking build outputs and artifacts.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    job = create_generic_fk(
        related_name="artifacts",
        to="gitlab_sync.GitLabSyncJob",
    )
    project = create_generic_fk(
        related_name="artifacts",
        to="gitlab_sync.GitLabSyncProject",
    )
    file_type: str | None = create_generic_varchar()
    size: int | None = create_generic_integer()
    filename: str | None = create_generic_varchar()
    file_format: str | None = create_generic_varchar()
    expire_at: datetime | None = create_generic_datetime()

    def __str__(self) -> str:
        return f"{self.filename} ({self.file_type})"

    class Meta:
        ordering = ["-id"]
        verbose_name = "GitLab Sync Artifact"
        verbose_name_plural = "GitLab Sync Artifacts"
