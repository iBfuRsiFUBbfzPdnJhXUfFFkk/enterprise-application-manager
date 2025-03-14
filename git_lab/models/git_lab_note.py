from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_text import create_generic_text
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class GitLabNote(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    author: GitLabUser | None = create_generic_fk(related_name="notes_authored", to=GitLabUser)
    body: str | None = create_generic_text()
    discussion: GitLabDiscussion | None = create_generic_fk(related_name="notes", to=GitLabDiscussion)
    group: GitLabGroup | None = create_generic_fk(related_name="notes", to=GitLabGroup)
    noteable_id: int | None = create_generic_integer()
    noteable_iid: int | None = create_generic_integer()
    noteable_type: str | None = create_generic_varchar()
    project: GitLabProject | None = create_generic_fk(related_name="notes", to=GitLabProject)
    scrum_sprint: ScrumSprint | None = create_generic_fk(related_name="notes", to=ScrumSprint)
    system: bool | None = create_generic_boolean()
    type: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Note"
        verbose_name_plural = "GitLab Notes"
