from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_state import AbstractGitLabState
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl


class GitLabUser(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabWebUrl,
    AbstractName,
):
    expires_at: datetime | None = create_generic_datetime()
    locked: bool | None = create_generic_boolean()
    username: str | None = create_generic_varchar()

    @property
    def issues_assigned(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(assignees__in=[self])
        )

    @property
    def issues_authored(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(author=self)
        )

    @property
    def issues_closed(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(closed_by=self)
        )

    @property
    def kpi_sprints(self):
        from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(group=self)
        )

    @property
    def merge_requests_assigned(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(assignees__in=[self])
        )

    @property
    def merge_requests_authored(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(author=self)
        )

    @property
    def merge_requests_closed(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(closed_by=self)
        )

    @property
    def merge_requests_merged(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(merged_by=self)
        )

    @property
    def merge_requests_reviewed(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(reviewers__in=[self])
        )

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        ordering = ['username']
        verbose_name = "GitLab User"
        verbose_name_plural = "GitLab Users"
