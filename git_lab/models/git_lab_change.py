from datetime import datetime

from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_references import AbstractGitLabReferences
from git_lab.models.common.abstract.abstract_git_lab_task_completion_status import AbstractGitLabTaskCompletionStatus
from git_lab.models.common.abstract.abstract_git_lab_time_stats import AbstractGitLabTimeStats
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser


class GitLabChange(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabReferences,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    assignees: set[GitLabUser] | None = create_generic_m2m(related_name="changes_assigned", to=GitLabUser)
    author: GitLabUser | None = create_generic_fk(related_name="changes_authored", to=GitLabUser)
    base_sha: str | None = create_generic_varchar()
    changes_count: str | None = create_generic_varchar()
    closed_by: GitLabUser | None = create_generic_fk(related_name="changes_closed", to=GitLabUser)
    draft: bool | None = create_generic_boolean()
    has_conflicts: bool | None = create_generic_boolean()
    head_sha: str | None = create_generic_varchar()
    latest_build_finished_at: datetime | None = create_generic_datetime()
    latest_build_started_at: datetime | None = create_generic_datetime()
    merge_commit_sha: str | None = create_generic_varchar()
    merged_at: datetime | None = create_generic_datetime()
    merged_by: GitLabUser | None = create_generic_fk(related_name="changes_merged", to=GitLabUser)
    prepared_at: datetime | None = create_generic_datetime()
    project: GitLabProject | None = create_generic_fk(related_name="changes", to=GitLabProject)
    sha: str | None = create_generic_varchar()
    squash_commit_sha: str | None = create_generic_varchar()
    start_sha: str | None = create_generic_varchar()
    state: str | None = create_generic_varchar()
    total_files_added: int | None = create_generic_integer()
    total_files_changed: int | None = create_generic_integer()
    total_files_deleted: int | None = create_generic_integer()
    total_files_generated: int | None = create_generic_integer()
    total_files_renamed: int | None = create_generic_integer()
    total_lines_added: int | None = create_generic_integer()
    total_lines_removed: int | None = create_generic_integer()


    def __str__(self) -> str:
        return f"{self.references_long}"

    class Meta:
        ordering = ['-id']
        verbose_name = "GitLab Change"
        verbose_name_plural = "GitLab Changes"
