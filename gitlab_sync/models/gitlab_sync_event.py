from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabCreatedAt,
    AbstractGitLabTitle,
)


class GitLabSyncEvent(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabTitle,
):
    """
    Represents a GitLab event (activity) synced from GitLab EE 17.11.6.

    Events track user activity like pushes, issues, merge requests, comments, etc.
    """

    gitlab_id: int | None = create_generic_integer()
    project = create_generic_fk(
        related_name="events",
        to="gitlab_sync.GitLabSyncProject",
    )
    author = create_generic_fk(
        related_name="events_authored",
        to="gitlab_sync.GitLabSyncUser",
    )
    action_name: str | None = create_generic_varchar()
    target_id: int | None = create_generic_integer()
    target_iid: int | None = create_generic_integer()
    target_type: str | None = create_generic_varchar()
    target_title: str | None = create_generic_varchar()
    push_data_commit_count: int | None = create_generic_integer()
    push_data_action: str | None = create_generic_varchar()
    push_data_ref_type: str | None = create_generic_varchar()
    push_data_commit_from: str | None = create_generic_varchar()
    push_data_commit_to: str | None = create_generic_varchar()
    push_data_ref: str | None = create_generic_varchar()
    push_data_commit_title: str | None = create_generic_varchar()

    def __str__(self) -> str:
        if self.action_name:
            return f"{self.action_name}: {self.target_title or self.title or 'Event'}"
        return f"Event {self.gitlab_id}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Event"
        verbose_name_plural = "GitLab Sync Events"
