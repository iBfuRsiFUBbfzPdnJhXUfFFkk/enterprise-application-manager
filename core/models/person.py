from datetime import date, datetime

from django.db.models import QuerySet

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_pronunciation import AbstractPronunciation
from core.models.common.abstract.abstract_scrum_capacity_base import AbstractScrumCapacityBase
from core.models.common.enums.job_level_choices import JOB_LEVEL_CHOICES
from core.models.common.enums.job_title_choices import JOB_TITLE_CHOICES
from core.models.common.enums.timezone_choices import TIMEZONE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.job_level import JobLevel
from core.models.job_title import JobTitle
from core.models.role import Role
from core.models.skill import Skill
from core.models.this_server_configuration import ThisServerConfiguration
from kpi.utilities.cast_query_set import cast_query_set


class Person(
    AbstractBaseModel,
    AbstractComment,
    AbstractLocation,
    AbstractPronunciation,
    AbstractScrumCapacityBase,
):
    communication_email: str | None = create_generic_varchar()
    date_birthday: date | None = create_generic_date()
    date_hired: date | None = create_generic_date()
    date_left: date | None = create_generic_date()
    gitlab_sync_access_level: str | None = create_generic_varchar()
    gitlab_sync_avatar_url: str | None = create_generic_varchar()
    gitlab_sync_datetime_created_at: datetime | None = create_generic_datetime()
    gitlab_sync_datetime_expires_at: datetime | None = create_generic_datetime()
    gitlab_sync_id: str | None = create_generic_varchar()
    gitlab_sync_is_locked: bool | None = create_generic_boolean()
    gitlab_sync_membership_state: str | None = create_generic_varchar()
    gitlab_sync_name: str | None = create_generic_varchar()
    gitlab_sync_state: str | None = create_generic_varchar()
    gitlab_sync_username: str | None = create_generic_varchar()
    gitlab_sync_web_url: str | None = create_generic_varchar()
    is_active: bool | None = create_generic_boolean(default=True)
    is_architect: bool | None = create_generic_boolean()
    is_bot: bool | None = create_generic_boolean()
    is_developer: bool | None = create_generic_boolean()
    is_employee: bool | None = create_generic_boolean(default=True)
    is_lead_developer: bool | None = create_generic_boolean()
    is_product_manager: bool | None = create_generic_boolean()
    is_product_owner: bool | None = create_generic_boolean()
    is_project_manager: bool | None = create_generic_boolean()
    is_scrum_master: bool | None = create_generic_boolean()
    is_stakeholder: bool | None = create_generic_boolean()
    link_sharepoint_profile: str | None = create_generic_varchar()
    job_level: JobLevel | None = create_generic_fk(to=JobLevel)
    job_title: JobLevel | None = create_generic_fk(to=JobTitle)
    name_first: str | None = create_generic_varchar()
    name_last: str | None = create_generic_varchar()
    name_preferred: str | None = create_generic_varchar()
    roles: list[Role] | None = create_generic_m2m(to=Role)
    skills: list[Skill] | None = create_generic_m2m(to=Skill)
    type_job_level: str | None = create_generic_enum(choices=JOB_LEVEL_CHOICES)
    type_job_title: str | None = create_generic_enum(choices=JOB_TITLE_CHOICES)
    type_timezone: str | None = create_generic_enum(choices=TIMEZONE_CHOICES)

    @property
    def coerced_communication_email(self) -> str | None:
        if self.communication_email is not None:
            return self.communication_email
        return self.user_mapping.email if self.user_mapping else None

    @property
    def coerced_name_first(self) -> str | None:
        if self.name_first is not None:
            return self.name_first
        return self.user_mapping.first_name if self.user_mapping else None

    @property
    def coerced_name_last(self) -> str | None:
        if self.name_last is not None:
            return self.name_last
        return self.user_mapping.last_name if self.user_mapping else None

    @property
    def coerced_scrum_capacity_base(self) -> int:
        if self.scrum_capacity_base is not None:
            return self.scrum_capacity_base
        return ThisServerConfiguration.current().coerced_scrum_capacity_base

    @property
    def full_name_for_human(self) -> str:
        return f"{self.coerced_name_first} {self.coerced_name_last}"

    @property
    def full_name_for_sort(self) -> str:
        return f"{self.coerced_name_last}, {self.coerced_name_first}"

    @property
    def groups(self):
        return self.user_mapping.groups if self.user_mapping else None

    @property
    def is_staff(self) -> bool:
        return self.user_mapping.is_staff if self.user_mapping else False

    @property
    def is_superuser(self) -> bool:
        return self.user_mapping.is_superuser if self.user_mapping else False

    @property
    def username(self) -> str | None:
        return self.user_mapping.username if self.user_mapping else None

    @property
    def user_mapping(self):
        from core.models.user import User
        return User.objects.filter(person_mapping=self).first()

    @property
    def user_permissions(self):
        return self.user_mapping.user_permissions if self.user_mapping else None

    @staticmethod
    def developers() -> QuerySet['Person']:
        developer_role: Role | None = ThisServerConfiguration.current().type_developer_role
        return cast_query_set(
            typ=Person,
            val=Person.objects.filter(roles__in=[developer_role]) if developer_role else Person.objects.all()
        )

    def __str__(self) -> str:
        title_particle: str = f" - {str(self.job_title)}" if self.job_title else ''
        return f"{self.full_name_for_sort}{title_particle}"

    class Meta:
        ordering = ['name_last', 'name_first', 'id']
        verbose_name = "Person"
        verbose_name_plural = "People"
