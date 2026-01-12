from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
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
    assignees: set[GitLabUser] | None = models.ManyToManyField(GitLabUser, blank=True, related_name="issues_assigned")
    author: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues_authored")
    blocking_issues_count: int | None = models.IntegerField(null=True, blank=True)
    closed_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues_closed")
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    has_tasks: bool | None = models.BooleanField(null=True, blank=True)
    issue_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    iteration: GitLabIteration | None = models.ForeignKey(GitLabIteration, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    link_award_emoji: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_notes: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_project: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_self: str | None = models.CharField(max_length=255, null=True, blank=True)
    project: GitLabProject | None = models.ForeignKey(GitLabProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    scrum_sprint: ScrumSprint | None = models.ForeignKey(ScrumSprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    type: str | None = models.CharField(max_length=255, null=True, blank=True)
    user_notes_count: int | None = models.IntegerField(null=True, blank=True)
    weight: int | None = models.IntegerField(null=True, blank=True)

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
