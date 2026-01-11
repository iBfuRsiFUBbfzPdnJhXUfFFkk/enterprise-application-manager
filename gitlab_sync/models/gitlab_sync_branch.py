from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
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

    project = create_generic_fk(
        related_name="branches",
        to="gitlab_sync.GitLabSyncProject",
    )
    repository = create_generic_fk(
        related_name="branches",
        to="gitlab_sync.GitLabSyncRepository",
    )
    commit_sha: str | None = create_generic_varchar()
    commit_short_id: str | None = create_generic_varchar()
    commit_title: str | None = create_generic_varchar()
    commit_message: str | None = create_generic_varchar()
    merged: bool | None = create_generic_boolean()
    protected: bool | None = create_generic_boolean()
    default: bool | None = create_generic_boolean()
    developers_can_push: bool | None = create_generic_boolean()
    developers_can_merge: bool | None = create_generic_boolean()
    can_push: bool | None = create_generic_boolean()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["-default", "name"]
        verbose_name = "GitLab Sync Branch"
        verbose_name_plural = "GitLab Sync Branches"
