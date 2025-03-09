from datetime import date

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup


class GitLabIteration(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    due_date: date | None = create_generic_date()
    group: GitLabGroup | None = create_generic_fk(related_name="iterations", to=GitLabGroup)
    sequence: int | None = create_generic_integer()
    start_date: date | None = create_generic_date()
    state: int | None = create_generic_integer()

    @property
    def issues(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(iteration=self)
        )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['-id']
        verbose_name = "GitLab Iteration"
        verbose_name_plural = "GitLab Iterations"
