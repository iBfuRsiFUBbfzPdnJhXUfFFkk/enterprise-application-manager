from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
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

    def __str__(self) -> str:
        return f"{self.full_path}"

    class Meta:
        ordering = ['full_path']
        verbose_name = "GitLab Group"
        verbose_name_plural = "GitLab Groups"
