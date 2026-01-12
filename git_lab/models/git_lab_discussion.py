from django.db import models

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
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="discussions")
    id: str = models.CharField(max_length=40, primary_key=True)
    individual_note: bool | None = models.BooleanField(null=True, blank=True)
    project: GitLabProject | None = models.ForeignKey(GitLabProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="discussions")
    scrum_sprint: ScrumSprint | None = models.ForeignKey(ScrumSprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="discussions")
    started_by: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="discussions_started")

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
