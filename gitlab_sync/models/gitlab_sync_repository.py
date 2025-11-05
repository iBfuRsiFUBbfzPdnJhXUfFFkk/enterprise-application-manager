from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class GitLabSyncRepository(AbstractBaseModel):
    """
    Represents a GitLab repository (code storage) for a project.

    New entity for tracking repository-specific data from GitLab EE 17.11.6.
    """

    project = create_generic_fk(
        related_name="repositories",
        to="gitlab_sync.GitLabSyncProject",
    )
    default_branch: str | None = create_generic_varchar()
    http_url_to_repo: str | None = create_generic_varchar()
    ssh_url_to_repo: str | None = create_generic_varchar()
    repository_size: int | None = create_generic_integer()
    lfs_size: int | None = create_generic_integer()
    storage_size: int | None = create_generic_integer()
    wiki_size: int | None = create_generic_integer()
    packages_size: int | None = create_generic_integer()
    snippets_size: int | None = create_generic_integer()

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
