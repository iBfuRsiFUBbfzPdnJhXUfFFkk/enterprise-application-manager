from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set


class GitLabSyncRepository(AbstractBaseModel):
    """
    Represents a GitLab repository (code storage) for a project.

    New entity for tracking repository-specific data from GitLab EE 17.11.6.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repositories",
    )
    default_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    http_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)
    ssh_url_to_repo: str | None = models.CharField(max_length=255, null=True, blank=True)
    repository_size: int | None = models.IntegerField(null=True, blank=True)
    lfs_size: int | None = models.IntegerField(null=True, blank=True)
    storage_size: int | None = models.IntegerField(null=True, blank=True)
    wiki_size: int | None = models.IntegerField(null=True, blank=True)
    packages_size: int | None = models.IntegerField(null=True, blank=True)
    snippets_size: int | None = models.IntegerField(null=True, blank=True)

    @property
    def commits(self):
        from gitlab_sync.models.gitlab_sync_commit import GitLabSyncCommit

        return cast_query_set(
            typ=GitLabSyncCommit, val=GitLabSyncCommit.objects.filter(repository=self)
        )

    @property
    def branches(self):
        from gitlab_sync.models.gitlab_sync_branch import GitLabSyncBranch

        return cast_query_set(
            typ=GitLabSyncBranch, val=GitLabSyncBranch.objects.filter(repository=self)
        )

    @property
    def tags(self):
        from gitlab_sync.models.gitlab_sync_tag import GitLabSyncTag

        return cast_query_set(
            typ=GitLabSyncTag, val=GitLabSyncTag.objects.filter(repository=self)
        )

    def __str__(self) -> str:
        if self.project:
            return f"Repository for {self.project.path_with_namespace}"
        return f"Repository {self.id}"

    class Meta:
        ordering = ["-id"]
        verbose_name = "GitLab Sync Repository"
        verbose_name_plural = "GitLab Sync Repositories"
