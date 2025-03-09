from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_state import AbstractGitLabState
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser


class GitLabMergeRequest(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    blocking_discussions_resolved: bool | None = create_generic_boolean()
    closed_at: datetime | None = create_generic_datetime()
    draft: bool | None = create_generic_boolean()
    has_conflicts: bool | None = create_generic_boolean()
    merged_at: datetime | None = create_generic_datetime()
    merged_by: GitLabUser | None = create_generic_fk(related_name="merge_requests_merged", to=GitLabUser)
    prepared_at: datetime | None = create_generic_datetime()
    project: GitLabProject | None = create_generic_fk(to=GitLabProject)
    references_long: str | None = create_generic_varchar()
    references_relative: str | None = create_generic_varchar()
    references_short: str | None = create_generic_varchar()
    reviewers: set[GitLabUser] | None = create_generic_m2m(to=GitLabUser)
    sha: str | None = create_generic_varchar()
    source_branch: str | None = create_generic_varchar()
    target_branch: str | None = create_generic_varchar()
    task_completion_status_completed_count: int | None = create_generic_integer()
    task_completion_status_count: int | None = create_generic_integer()
    time_stats_human_time_estimate: str | None = create_generic_varchar()
    time_stats_human_total_time_spent: str | None = create_generic_varchar()
    time_stats_time_estimate: int | None = create_generic_integer()
    time_stats_total_time_spent: int | None = create_generic_integer()
    title: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.references_relative}"

    class Meta:
        ordering = ['-id']
        verbose_name = "GitLab Merge Request"
        verbose_name_plural = "GitLab Merge Requests"
