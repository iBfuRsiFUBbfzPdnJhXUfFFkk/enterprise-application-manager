from datetime import datetime

from django.db import models

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
    assignees: set[GitLabUser] | None = models.ManyToManyField(GitLabUser, blank=True, related_name="merge_requests_assigned")
    author: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests_authored")
    blocking_discussions_resolved: bool | None = models.BooleanField(null=True, blank=True)
    closed_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests_closed")
    draft: bool | None = models.BooleanField(null=True, blank=True)
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests")
    has_conflicts: bool | None = models.BooleanField(null=True, blank=True)
    merged_at: datetime | None = models.DateTimeField(null=True, blank=True)
    merged_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests_merged")
    prepared_at: datetime | None = models.DateTimeField(null=True, blank=True)
    project: GitLabProject | None = models.ForeignKey(GitLabProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests")
    reviewers: set[GitLabUser] | None = models.ManyToManyField(GitLabUser, blank=True, related_name="merge_requests_reviewed")
    sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    source_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    scrum_sprint: ScrumSprint | None = models.ForeignKey(ScrumSprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="merge_requests")
    target_branch: str | None = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.references_relative}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Merge Request"
        verbose_name_plural = "GitLab Merge Requests"
