from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
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

    project = create_generic_fk(
        related_name="snippets",
        to="gitlab_sync.GitLabSyncProject",
    )
    author = create_generic_fk(
        related_name="snippets",
        to="gitlab_sync.GitLabSyncUser",
    )
    gitlab_id: int | None = create_generic_integer()
    title: str | None = create_generic_varchar()
    file_name: str | None = create_generic_varchar()
    description: str | None = create_generic_varchar()
    visibility: str | None = create_generic_enum(
        choices=[
            ("private", "Private"),
            ("internal", "Internal"),
            ("public", "Public"),
        ]
    )
    raw_url: str | None = create_generic_varchar()
    created_at: datetime | None = create_generic_datetime()
    updated_at: datetime | None = create_generic_datetime()

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "GitLab Sync Snippet"
        verbose_name_plural = "GitLab Sync Snippets"
