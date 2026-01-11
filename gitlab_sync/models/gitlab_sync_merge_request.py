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
    AbstractGitLabReferences,
    AbstractGitLabState,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncMergeRequest(
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
    Represents a GitLab merge request synced from GitLab EE 17.11.6.

    Improved implementation with enhanced pipeline and code review tracking.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    assignees = create_generic_m2m(
        related_name="merge_requests_assigned",
        to="gitlab_sync.GitLabSyncUser",
    )
    author = create_generic_fk(
        related_name="merge_requests_authored",
        to="gitlab_sync.GitLabSyncUser",
    )
    closed_by = create_generic_fk(
        related_name="merge_requests_closed",
        to="gitlab_sync.GitLabSyncUser",
    )
    merged_by = create_generic_fk(
        related_name="merge_requests_merged",
        to="gitlab_sync.GitLabSyncUser",
    )
    reviewers = create_generic_m2m(
        related_name="merge_requests_reviewed",
        to="gitlab_sync.GitLabSyncUser",
    )
    group = create_generic_fk(
        related_name="merge_requests",
        to="gitlab_sync.GitLabSyncGroup",
    )
    project = create_generic_fk(
        related_name="merge_requests",
        to="gitlab_sync.GitLabSyncProject",
    )
    head_pipeline = create_generic_fk(
        related_name="merge_requests",
        to="gitlab_sync.GitLabSyncPipeline",
    )
    milestone = create_generic_fk(
        related_name="merge_requests",
        to="gitlab_sync.GitLabSyncMilestone",
    )
    iteration = create_generic_fk(
        related_name="merge_requests",
        to="gitlab_sync.GitLabSyncIteration",
    )
    blocking_discussions_resolved: bool | None = create_generic_boolean()
    draft: bool | None = create_generic_boolean()
    has_conflicts: bool | None = create_generic_boolean()
    merged_at: datetime | None = create_generic_datetime()
    prepared_at: datetime | None = create_generic_datetime()
    sha: str | None = create_generic_varchar()
    source_branch: str | None = create_generic_varchar()
    target_branch: str | None = create_generic_varchar()
    squash: bool | None = create_generic_boolean()
    squash_commit_sha: str | None = create_generic_varchar()
    merge_status: str | None = create_generic_varchar()
    diff_refs_base_sha: str | None = create_generic_varchar()
    diff_refs_head_sha: str | None = create_generic_varchar()
    diff_refs_start_sha: str | None = create_generic_varchar()
    user_notes_count: int | None = create_generic_integer()
    upvotes: int | None = create_generic_integer()
    downvotes: int | None = create_generic_integer()

    @property
    def pipelines(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline,
            val=GitLabSyncPipeline.objects.filter(merge_request=self),
        )

    def __str__(self) -> str:
        return f"!{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Merge Request"
        verbose_name_plural = "GitLab Sync Merge Requests"
