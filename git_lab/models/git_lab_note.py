from django.db import models

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
    author: GitLabUser | None = models.ForeignKey(GitLabUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes_authored")
    body: str | None = models.TextField(null=True, blank=True)
    discussion: GitLabDiscussion | None = models.ForeignKey(GitLabDiscussion, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    group: GitLabGroup | None = models.ForeignKey(GitLabGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    noteable_id: int | None = models.IntegerField(null=True, blank=True)
    noteable_iid: int | None = models.IntegerField(null=True, blank=True)
    noteable_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    project: GitLabProject | None = models.ForeignKey(GitLabProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    scrum_sprint: ScrumSprint | None = models.ForeignKey(ScrumSprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    system: bool | None = models.BooleanField(null=True, blank=True)
    type: str | None = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "GitLab Note"
        verbose_name_plural = "GitLab Notes"
