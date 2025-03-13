from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl


class GitLabGroup(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
    AbstractName,
):
    full_name: str | None = create_generic_varchar()
    full_path: str | None = create_generic_varchar()

    @property
    def issues(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(group=self)
        )

    @property
    def iterations(self):
        from git_lab.models.git_lab_iteration import GitLabIteration
        return cast_query_set(
            typ=GitLabIteration,
            val=GitLabIteration.objects.filter(group=self)
        )

    @property
    def projects(self):
        from git_lab.models.git_lab_project import GitLabProject
        return cast_query_set(
            typ=GitLabProject,
            val=GitLabProject.objects.filter(group=self)
        )

    def __str__(self) -> str:
        return f"{self.full_path}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "GitLab Group"
        verbose_name_plural = "GitLab Groups"
