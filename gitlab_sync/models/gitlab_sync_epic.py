from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncEpic(
    AbstractBaseModel,
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    """
    Represents a GitLab Epic (Enterprise Edition feature) from GitLab EE 17.11.6.

    Epics are high-level organizational items that group related issues.
    Only available in GitLab Enterprise Edition.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    group = create_generic_fk(
        related_name="epics",
        to="gitlab_sync.GitLabSyncGroup",
    )
    author = create_generic_fk(
        related_name="epics_authored",
        to="gitlab_sync.GitLabSyncUser",
    )
    parent_epic = create_generic_fk(
        related_name="child_epics",
        to="gitlab_sync.GitLabSyncEpic",
    )
    # labels field removed - core.Label model doesn't exist
    # can be added later if needed
    start_date: datetime | None = create_generic_datetime()
    end_date: datetime | None = create_generic_datetime()
    start_date_is_fixed: bool | None = create_generic_boolean()
    start_date_fixed: datetime | None = create_generic_datetime()
    start_date_from_inherited_source: datetime | None = create_generic_datetime()
    due_date: datetime | None = create_generic_datetime()
    due_date_is_fixed: bool | None = create_generic_boolean()
    due_date_fixed: datetime | None = create_generic_datetime()
    due_date_from_inherited_source: datetime | None = create_generic_datetime()
    upvotes: int | None = create_generic_integer()
    downvotes: int | None = create_generic_integer()
    user_notes_count: int | None = create_generic_integer()
    confidential: bool | None = create_generic_boolean()
    color: str | None = create_generic_varchar()

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(epic=self)
        )

    def __str__(self) -> str:
        return f"Epic &{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Epic"
        verbose_name_plural = "GitLab Sync Epics"
