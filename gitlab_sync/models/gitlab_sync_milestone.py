from datetime import date, datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import AbstractGitLabWebUrl


class GitLabSyncMilestone(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a milestone (project or group) synced from GitLab EE 17.11.6.

    Milestones are used to track issues and merge requests over a period of time.
    """

    project = create_generic_fk(
        related_name="milestones",
        to="gitlab_sync.GitLabSyncProject",
    )
    group = create_generic_fk(
        related_name="milestones",
        to="gitlab_sync.GitLabSyncGroup",
    )
    gitlab_id: int | None = create_generic_integer()
    title: str | None = create_generic_varchar()
    description: str | None = create_generic_varchar()
    state: str | None = create_generic_enum(
        choices=[
            ("active", "Active"),
            ("closed", "Closed"),
        ]
    )
    due_date: date | None = create_generic_date()
    start_date: date | None = create_generic_date()
    created_at: datetime | None = create_generic_datetime()
    updated_at: datetime | None = create_generic_datetime()

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(milestone=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(milestone=self),
        )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-due_date", "-created_at"]
        verbose_name = "GitLab Sync Milestone"
        verbose_name_plural = "GitLab Sync Milestones"
