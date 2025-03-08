from datetime import datetime

from django.db.models import IntegerField

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class GitLabProject(
    AbstractBaseModel,
    AbstractName,
):
    avatar_url: str | None = create_generic_varchar()
    container_registry_image_prefix: str | None = create_generic_varchar()
    created_at: datetime | None = create_generic_datetime()
    default_branch: str | None = create_generic_varchar()
    description: str | None = create_generic_varchar()
    http_url_to_repo: str | None = create_generic_varchar()
    id: int = IntegerField(primary_key=True)
    last_activity_at: datetime | None = create_generic_datetime()
    link_cluster_agents: str | None = create_generic_varchar()
    link_events: str | None = create_generic_varchar()
    link_issues: str | None = create_generic_varchar()
    link_labels: str | None = create_generic_varchar()
    link_members: str | None = create_generic_varchar()
    link_merge_requests: str | None = create_generic_varchar()
    link_repo_branches: str | None = create_generic_varchar()
    link_self: str | None = create_generic_varchar()
    name_with_namespace: str | None = create_generic_varchar()
    open_issues_count: int | None = create_generic_integer()
    path: str | None = create_generic_varchar()
    path_with_namespace: str | None = create_generic_varchar()
    readme_url: str | None = create_generic_varchar()
    ssh_url_to_repo: str | None = create_generic_varchar()
    updated_at: datetime | None = create_generic_datetime()
    web_url: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ['path_with_namespace']
        verbose_name = "GitLab Project"
        verbose_name_plural = "GitLab Projects"
