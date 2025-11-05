from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
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

    sha: str | None = create_generic_varchar()
    short_id: str | None = create_generic_varchar()
    author = create_generic_fk(
        related_name="commits_authored",
        to="gitlab_sync.GitLabSyncUser",
    )
    author_name: str | None = create_generic_varchar()
    author_email: str | None = create_generic_varchar()
    authored_date: datetime | None = create_generic_datetime()
    committer_name: str | None = create_generic_varchar()
    committer_email: str | None = create_generic_varchar()
    committed_date: datetime | None = create_generic_datetime()
    project = create_generic_fk(
        related_name="commits",
        to="gitlab_sync.GitLabSyncProject",
    )
    repository = create_generic_fk(
        related_name="commits",
        to="gitlab_sync.GitLabSyncRepository",
    )
    message: str | None = create_generic_varchar()
    parent_ids: str | None = create_generic_varchar()
    additions: int | None = create_generic_integer()
    deletions: int | None = create_generic_integer()
    total_changes: int | None = create_generic_integer()

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
