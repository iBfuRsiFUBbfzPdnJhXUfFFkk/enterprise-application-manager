from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class GitLabSyncTag(
    AbstractBaseModel,
    AbstractName,
):
    """
    Represents a Git tag (version release) synced from GitLab EE 17.11.6.

    New entity for tracking releases and version tags.
    """

    project = create_generic_fk(
        related_name="tags",
        to="gitlab_sync.GitLabSyncProject",
    )
    repository = create_generic_fk(
        related_name="tags",
        to="gitlab_sync.GitLabSyncRepository",
    )
    commit_sha: str | None = create_generic_varchar()
    commit_short_id: str | None = create_generic_varchar()
    commit_title: str | None = create_generic_varchar()
    commit_message: str | None = create_generic_varchar()
    commit_created_at: datetime | None = create_generic_datetime()
    message: str | None = create_generic_varchar()
    release_description: str | None = create_generic_varchar()
    protected: bool | None = create_generic_boolean()
    target: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["-commit_created_at"]
        verbose_name = "GitLab Sync Tag"
        verbose_name_plural = "GitLab Sync Tags"
