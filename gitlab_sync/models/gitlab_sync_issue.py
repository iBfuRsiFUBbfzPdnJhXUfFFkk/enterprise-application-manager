from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
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
    AbstractGitLabReferences,
    AbstractGitLabState,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncIssue(
    AbstractBaseModel,
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabReferences,
    AbstractGitLabState,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    """
    Represents a GitLab issue synced from GitLab EE 17.11.6.

    Improved implementation with better tracking and validation.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    assignees = create_generic_m2m(
        related_name="issues_assigned",
        to="gitlab_sync.GitLabSyncUser",
    )
    author = create_generic_fk(
        related_name="issues_authored",
        to="gitlab_sync.GitLabSyncUser",
    )
    closed_by = create_generic_fk(
        related_name="issues_closed",
        to="gitlab_sync.GitLabSyncUser",
    )
    group = create_generic_fk(
        related_name="issues",
        to="gitlab_sync.GitLabSyncGroup",
    )
    project = create_generic_fk(
        related_name="issues",
        to="gitlab_sync.GitLabSyncProject",
    )
    epic = create_generic_fk(
        related_name="issues",
        to="gitlab_sync.GitLabSyncEpic",
    )
    milestone = create_generic_fk(
        related_name="issues",
        to="gitlab_sync.GitLabSyncMilestone",
    )
    iteration = create_generic_fk(
        related_name="issues",
        to="gitlab_sync.GitLabSyncIteration",
    )
    blocking_issues_count: int | None = create_generic_integer()
    has_tasks: bool | None = create_generic_boolean()
    issue_type: str | None = create_generic_varchar()
    type: str | None = create_generic_varchar()
    user_notes_count: int | None = create_generic_integer()
    weight: int | None = create_generic_integer()
    severity: str | None = create_generic_varchar()
    due_date: str | None = create_generic_varchar()
    confidential: bool | None = create_generic_boolean()

    def __str__(self) -> str:
        return f"#{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Issue"
        verbose_name_plural = "GitLab Sync Issues"
