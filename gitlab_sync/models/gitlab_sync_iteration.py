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


class GitLabSyncIteration(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents an iteration (group-level sprint) synced from GitLab EE 17.11.6.

    Iterations are used for agile planning and tracking work over time periods.
    """

    group = create_generic_fk(
        related_name="iterations",
        to="gitlab_sync.GitLabSyncGroup",
    )
    gitlab_id: int | None = create_generic_integer()
    title: str | None = create_generic_varchar()
    description: str | None = create_generic_varchar()
    state: str | None = create_generic_enum(
        choices=[
            ("upcoming", "Upcoming"),
            ("started", "Started"),
            ("closed", "Closed"),
        ]
    )
    due_date: date | None = create_generic_date()
    start_date: date | None = create_generic_date()
    sequence: int | None = create_generic_integer()
    created_at: datetime | None = create_generic_datetime()
    updated_at: datetime | None = create_generic_datetime()

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(iteration=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(iteration=self),
        )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-start_date", "-sequence"]
        verbose_name = "GitLab Sync Iteration"
        verbose_name_plural = "GitLab Sync Iterations"
