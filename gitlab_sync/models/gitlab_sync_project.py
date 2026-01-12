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
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncProject(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a GitLab project synced from GitLab EE 17.11.6.

    Improved implementation with enhanced repository tracking capabilities.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    application = models.ForeignKey(
        "core.Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gitlab_sync_projects",
    )
    container_registry_image_prefix: str | None = models.CharField(max_length=255, null=True, blank=True)
    default_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    http_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)
    last_activity_at: datetime | None = models.DateTimeField(null=True, blank=True)
    name_with_namespace: str | None = models.CharField(max_length=255, null=True, blank=True)
    open_issues_count: int | None = models.IntegerField(null=True, blank=True)
    path_with_namespace: str | None = models.CharField(max_length=255, null=True, blank=True)
    readme_url: str | None = models.CharField(max_length=255, null=True, blank=True)
    ssh_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)
    visibility: str | None = models.CharField(max_length=255, null=True, blank=True)
    archived: bool | None = models.BooleanField(null=True, blank=True)
    star_count: int | None = models.IntegerField(null=True, blank=True)
    forks_count: int | None = models.IntegerField(null=True, blank=True)
    last_synced_at: datetime | None = models.DateTimeField(null=True, blank=True)

    @property
    def repository(self):
        from gitlab_sync.models.gitlab_sync_repository import GitLabSyncRepository

        return GitLabSyncRepository.objects.filter(project=self).first()

    @property
    def commits(self):
        from gitlab_sync.models.gitlab_sync_commit import GitLabSyncCommit

        return cast_query_set(
            typ=GitLabSyncCommit, val=GitLabSyncCommit.objects.filter(project=self)
        )

    @property
    def branches(self):
        from gitlab_sync.models.gitlab_sync_branch import GitLabSyncBranch

        return cast_query_set(
            typ=GitLabSyncBranch, val=GitLabSyncBranch.objects.filter(project=self)
        )

    @property
    def pipelines(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline, val=GitLabSyncPipeline.objects.filter(project=self)
        )

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(project=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(project=self),
        )

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Project"
        verbose_name_plural = "GitLab Sync Projects"
