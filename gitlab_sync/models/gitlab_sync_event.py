from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
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

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    gitlab_id: int | None = models.IntegerField(null=True, blank=True)
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events_authored",
    )
    action_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    target_id: int | None = models.IntegerField(null=True, blank=True)
    target_iid: int | None = models.IntegerField(null=True, blank=True)
    target_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    target_title: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_commit_count: int | None = models.IntegerField(null=True, blank=True)
    push_data_action: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_ref_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_commit_from: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_commit_to: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_ref: str | None = models.CharField(max_length=255, null=True, blank=True)
    push_data_commit_title: str | None = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        if self.action_name:
            return f"{self.action_name}: {self.target_title or self.title or 'Event'}"
        return f"Event {self.gitlab_id}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Event"
        verbose_name_plural = "GitLab Sync Events"
