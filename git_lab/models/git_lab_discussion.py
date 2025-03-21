from django.db.models import CharField
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class GitLabDiscussion(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabUpdatedAt,
):
    group: GitLabGroup | None = create_generic_fk(related_name="discussions", to=GitLabGroup)
    id: str = CharField(max_length=40, primary_key=True)
    individual_note: bool | None = create_generic_boolean()
    project: GitLabProject | None = create_generic_fk(related_name="discussions", to=GitLabProject)
    scrum_sprint: ScrumSprint | None = create_generic_fk(related_name="discussions", to=ScrumSprint)
    started_by: GitLabUser | None = create_generic_fk(related_name="discussions_started", to=GitLabUser)

    @property
    def notes(self):
        from git_lab.models.git_lab_note import GitLabNote
        return GitLabNote.objects.filter(discussion=self)

    def __str__(self) -> str:
        return f"{self.id}"

    class Meta:
        ordering = ['-updated_at', '-id']
        verbose_name = "GitLab Discussion"
        verbose_name_plural = "GitLab Discussions"
