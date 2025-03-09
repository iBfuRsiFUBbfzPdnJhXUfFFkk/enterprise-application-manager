from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
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

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        ordering = ['username']
        verbose_name = "GitLab User"
        verbose_name_plural = "GitLab Users"
