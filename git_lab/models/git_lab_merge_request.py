from datetime import datetime

from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from git_lab.models.common.abstract.abstract_git_lab_closed_at import AbstractGitLabClosedAt
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_references import AbstractGitLabReferences
from git_lab.models.common.abstract.abstract_git_lab_state import AbstractGitLabState
from git_lab.models.common.abstract.abstract_git_lab_task_completion_status import AbstractGitLabTaskCompletionStatus
from git_lab.models.common.abstract.abstract_git_lab_time_stats import AbstractGitLabTimeStats
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class GitLabMergeRequest(
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
    assignees: set[GitLabUser] | None = create_generic_m2m(related_name="merge_requests_assigned", to=GitLabUser)
    author: GitLabUser | None = create_generic_fk(related_name="merge_requests_authored", to=GitLabUser)
    blocking_discussions_resolved: bool | None = create_generic_boolean()
    closed_by: GitLabUser | None = create_generic_fk(related_name="merge_requests_closed", to=GitLabUser)
    draft: bool | None = create_generic_boolean()
    group: GitLabGroup | None = create_generic_fk(related_name="merge_requests", to=GitLabGroup)
    has_conflicts: bool | None = create_generic_boolean()
    merged_at: datetime | None = create_generic_datetime()
    merged_by: GitLabUser | None = create_generic_fk(related_name="merge_requests_merged", to=GitLabUser)
    prepared_at: datetime | None = create_generic_datetime()
    project: GitLabProject | None = create_generic_fk(related_name="merge_requests", to=GitLabProject)
    reviewers: set[GitLabUser] | None = create_generic_m2m(related_name="merge_requests_reviewed", to=GitLabUser)
    sha: str | None = create_generic_varchar()
    source_branch: str | None = create_generic_varchar()
    scrum_sprint: ScrumSprint | None = create_generic_fk(related_name="merge_requests", to=ScrumSprint)
    target_branch: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.references_relative}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Merge Request"
        verbose_name_plural = "GitLab Merge Requests"
