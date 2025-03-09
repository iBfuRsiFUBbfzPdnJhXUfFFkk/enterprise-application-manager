from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl


class GitLabGroup(
    AbstractBaseModel,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
    AbstractName,
):
    avatar_url: str | None = create_generic_varchar()
    created_at: datetime | None = create_generic_datetime()
    description: str | None = create_generic_varchar()
    full_name: str | None = create_generic_varchar()
    full_path: str | None = create_generic_varchar()
    path: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.full_path}"

    class Meta:
        ordering = ['full_path']
        verbose_name = "GitLab Group"
        verbose_name_plural = "GitLab Groups"
