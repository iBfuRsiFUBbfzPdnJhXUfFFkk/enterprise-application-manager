from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_references import AbstractGitLabReferences
from git_lab.models.common.abstract.abstract_git_lab_task_completion_status import AbstractGitLabTaskCompletionStatus
from git_lab.models.common.abstract.abstract_git_lab_time_stats import AbstractGitLabTimeStats
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


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
    assignees: set[GitLabUser] | None = models.ManyToManyField(GitLabUser, blank=True, related_name="changes_assigned")
    author: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes_authored")
    base_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    changes_count: str | None = models.CharField(max_length=255, null=True, blank=True)
    closed_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes_closed")
    draft: bool | None = models.BooleanField(null=True, blank=True)
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes")
    has_conflicts: bool | None = models.BooleanField(null=True, blank=True)
    head_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    latest_build_finished_at: datetime | None = models.DateTimeField(null=True, blank=True)
    latest_build_started_at: datetime | None = models.DateTimeField(null=True, blank=True)
    merge_commit_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    merged_at: datetime | None = models.DateTimeField(null=True, blank=True)
    merged_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes_merged")
    prepared_at: datetime | None = models.DateTimeField(null=True, blank=True)
    project: GitLabProject | None = models.ForeignKey(GitLabProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes")
    scrum_sprint: ScrumSprint | None = models.ForeignKey(ScrumSprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="changes")
    sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    squash_commit_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    start_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    state: str | None = models.CharField(max_length=255, null=True, blank=True)
    total_files_added: int | None = models.IntegerField(null=True, blank=True)
    total_files_changed: int | None = models.IntegerField(null=True, blank=True)
    total_files_deleted: int | None = models.IntegerField(null=True, blank=True)
    total_files_generated: int | None = models.IntegerField(null=True, blank=True)
    total_files_renamed: int | None = models.IntegerField(null=True, blank=True)
    total_files_updated: int | None = models.IntegerField(null=True, blank=True)
    total_lines_added: int | None = models.IntegerField(null=True, blank=True)
    total_lines_removed: int | None = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.references_long}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Change"
        verbose_name_plural = "GitLab Changes"
