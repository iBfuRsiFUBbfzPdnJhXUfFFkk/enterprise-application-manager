from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup


class GitLabProject(
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
    container_registry_image_prefix: str | None = models.CharField(max_length=255, null=True, blank=True)
    default_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    http_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)
    last_activity_at: datetime | None = models.DateTimeField(null=True, blank=True)
    link_cluster_agents: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_events: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_issues: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_labels: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_members: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_merge_requests: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_repo_branches: str | None = models.CharField(max_length=255, null=True, blank=True)
    link_self: str | None = models.CharField(max_length=255, null=True, blank=True)
    name_with_namespace: str | None = models.CharField(max_length=255, null=True, blank=True)
    open_issues_count: int | None = models.IntegerField(null=True, blank=True)
    path_with_namespace: str | None = models.CharField(max_length=255, null=True, blank=True)
    readme_url: str | None = models.CharField(max_length=255, null=True, blank=True)
    should_skip: bool | None = models.BooleanField(null=True, blank=True)
    ssh_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)

    @property
    def changes(self):
        from git_lab.models.git_lab_change import GitLabChange
        return cast_query_set(
            typ=GitLabChange,
            val=GitLabChange.objects.filter(project=self)
        )

    @property
    def discussions(self):
        from git_lab.models.git_lab_discussion import GitLabDiscussion
        return cast_query_set(
            typ=GitLabDiscussion,
            val=GitLabDiscussion.objects.filter(project=self)
        )

    @property
    def issues(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(project=self)
        )

    @property
    def merge_requests(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(project=self)
        )

    @property
    def notes(self):
        from git_lab.models.git_lab_note import GitLabNote
        return cast_query_set(
            typ=GitLabNote,
            val=GitLabNote.objects.filter(project=self)
        )

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Project"
        verbose_name_plural = "GitLab Projects"
