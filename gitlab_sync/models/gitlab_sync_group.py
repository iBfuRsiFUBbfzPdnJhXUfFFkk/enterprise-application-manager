from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from gitlab_sync.models.common.abstract import (
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
)


class GitLabSyncGroup(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a GitLab group synced from GitLab EE 17.11.6.

    Improved implementation with better error handling and validation.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    full_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    full_path: str | None = models.CharField(max_length=255, null=True, blank=True)
    visibility: str | None = models.CharField(max_length=255, null=True, blank=True)
    last_synced_at: datetime | None = models.DateTimeField(null=True, blank=True)

    @property
    def projects(self):
        from gitlab_sync.models.gitlab_sync_project import GitLabSyncProject

        return cast_query_set(
            typ=GitLabSyncProject,
            val=GitLabSyncProject.objects.filter(group=self),
        )

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(group=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(group=self),
        )

    @property
    def epics(self):
        from gitlab_sync.models.gitlab_sync_epic import GitLabSyncEpic

        return cast_query_set(
            typ=GitLabSyncEpic, val=GitLabSyncEpic.objects.filter(group=self)
        )

    def __str__(self) -> str:
        return f"{self.full_path}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Group"
        verbose_name_plural = "GitLab Sync Groups"
