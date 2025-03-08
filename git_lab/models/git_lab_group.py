from datetime import datetime

from django.db.models import IntegerField

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class GitLabGroup(
    AbstractBaseModel,
    AbstractName,
):
    avatar_url: str | None = create_generic_varchar()
    created_at: datetime | None = create_generic_datetime()
    description: str | None = create_generic_varchar()
    full_name: str | None = create_generic_varchar()
    full_path: str | None = create_generic_varchar()
    id: int = IntegerField(primary_key=True)
    path: str | None = create_generic_varchar()
    web_url: str | None = create_generic_varchar()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['full_path']
        verbose_name = "GitLab Group"
        verbose_name_plural = "GitLab Groups"
