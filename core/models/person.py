from datetime import date, datetime

from django.db.models import QuerySet
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_pronunciation import AbstractPronunciation
from core.models.common.abstract.abstract_scrum_capacity_base import AbstractScrumCapacityBase
from core.models.common.enums.job_level_choices import JOB_LEVEL_CHOICES
from core.models.common.enums.job_title_choices import JOB_TITLE_CHOICES
from core.models.common.enums.timezone_choices import TIMEZONE_CHOICES
from core.models.job_level import JobLevel
from core.models.job_title import JobTitle
from core.models.role import Role
from core.models.skill import Skill
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set

class Person(
    AbstractBaseModel,
    AbstractComment,
    AbstractLocation,
    AbstractPronunciation,
    AbstractScrumCapacityBase,
):
    communication_email: str | None = models.CharField(max_length=255, null=True, blank=True)
    date_birthday: date | None = models.DateField(null=True, blank=True)
    date_hired: date | None = models.DateField(null=True, blank=True)
    date_left: date | None = models.DateField(null=True, blank=True)
    gitlab_sync_access_level: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_avatar_url: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_datetime_created_at: datetime | None = models.DateTimeField(null=True, blank=True)
    gitlab_sync_datetime_expires_at: datetime | None = models.DateTimeField(null=True, blank=True)
    gitlab_sync_id: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_is_locked: bool | None = models.BooleanField(null=True, blank=True)
    gitlab_sync_membership_state: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_state: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_username: str | None = models.CharField(max_length=255, null=True, blank=True)
    gitlab_sync_web_url: str | None = models.CharField(max_length=255, null=True, blank=True)
    is_active: bool | None = models.BooleanField(null=True, blank=True, default=True)
    is_bot: bool | None = models.BooleanField(null=True, blank=True)
    is_employee: bool | None = models.BooleanField(null=True, blank=True, default=True)
    link_sharepoint_profile: str | None = models.CharField(max_length=255, null=True, blank=True)
    job_level: JobLevel | None = models.ForeignKey(JobLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_set")
    job_title: JobLevel | None = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_set")
    name_first: str | None = models.CharField(max_length=255, null=True, blank=True)
    name_last: str | None = models.CharField(max_length=255, null=True, blank=True)
    name_preferred: str | None = models.CharField(max_length=255, null=True, blank=True)
    roles: list[Role] | None = models.ManyToManyField(Role, blank=True, related_name="%(class)s_set")
    skills: list[Skill] | None = models.ManyToManyField(Skill, blank=True, related_name="%(class)s_set")
    type_job_level: str | None = models.CharField(max_length=255, choices=JOB_LEVEL_CHOICES, null=True, blank=True)
    type_job_title: str | None = models.CharField(max_length=255, choices=JOB_TITLE_CHOICES, null=True, blank=True)
    type_timezone: str | None = models.CharField(max_length=255, choices=TIMEZONE_CHOICES, null=True, blank=True)

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
    def organizations(self):
        from core.models.organization import Organization
        return cast_query_set(
            typ=Organization,
            val=Organization.objects.filter(people__in=[self])
        )

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

    @staticmethod
    def developers_active() -> QuerySet['Person']:
        return cast_query_set(
            typ=Person,
            val=Person.developers().filter(is_active=True)
        )

    @staticmethod
    def developers_actively_employed() -> QuerySet['Person']:
        return cast_query_set(
            typ=Person,
            val=Person.developers_active().filter(is_employee=True)
        )

    def __str__(self) -> str:
        title_particle: str = f" - {str(self.job_title)}" if self.job_title else ''
        return f"{self.full_name_for_sort}{title_particle}"

    class Meta:
        ordering = ['name_last', 'name_first', 'id']
        verbose_name = "Person"
        verbose_name_plural = "People"
