from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.utilities.cast_query_set import cast_query_set
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
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class GitLabIssue(
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
    assignees: set[GitLabUser] | None = create_generic_m2m(related_name="issues_assigned", to=GitLabUser)
    author: GitLabUser | None = create_generic_fk(related_name="issues_authored", to=GitLabUser)
    blocking_issues_count: int | None = create_generic_integer()
    closed_by: GitLabUser | None = create_generic_fk(related_name="issues_closed", to=GitLabUser)
    group: GitLabGroup | None = create_generic_fk(related_name="issues", to=GitLabGroup)
    has_tasks: bool | None = create_generic_boolean()
    issue_type: str | None = create_generic_varchar()
    iteration: GitLabIteration | None = create_generic_fk(related_name="issues", to=GitLabIteration)
    link_award_emoji: str | None = create_generic_varchar()
    link_notes: str | None = create_generic_varchar()
    link_project: str | None = create_generic_varchar()
    link_self: str | None = create_generic_varchar()
    project: GitLabProject | None = create_generic_fk(related_name="issues", to=GitLabProject)
    scrum_sprint: ScrumSprint | None = create_generic_fk(related_name="issues", to=ScrumSprint)
    type: str | None = create_generic_varchar()
    user_notes_count: int | None = create_generic_integer()
    weight: int | None = create_generic_integer()

    @property
    def kpi_sprints(self):
        from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(git_lab_issues__in=[self])
        )

    def __str__(self) -> str:
        return f"{self.references_long}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Issue"
        verbose_name_plural = "GitLab Issues"
