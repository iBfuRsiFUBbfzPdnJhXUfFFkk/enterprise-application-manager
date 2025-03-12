from django.db.models import CharField
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from git_lab.models.git_lab_project import GitLabProject


class GitLabDiscussion(
    AbstractBaseModel
):
    id: str = CharField(max_length=40, primary_key=True)
    individual_note: bool | None = create_generic_boolean()
    project: GitLabProject | None = create_generic_fk(related_name="discussions", to=GitLabProject)

    @property
    def notes(self):
        from git_lab.models.git_lab_note import GitLabNote
        return GitLabNote.objects.filter(discussion=self)

    def __str__(self) -> str:
        return f"{self.id}"

    class Meta:
        ordering = ['-id']
        verbose_name = "GitLab Discussion"
        verbose_name_plural = "GitLab Discussions"
