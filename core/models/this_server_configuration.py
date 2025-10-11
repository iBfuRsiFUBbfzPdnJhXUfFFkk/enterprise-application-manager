from math import ceil

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_scrum_capacity_base import AbstractScrumCapacityBase
from core.models.common.enums.git_lab_api_version_choices import GIT_LAB_API_VERSION_CHOICES, GIT_LAB_API_VERSION_FOUR
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.models.role import Role
from core.models.secret import Secret


class ThisServerConfiguration(
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractScrumCapacityBase,
):
    connection_git_lab_api_version: str | None = create_generic_enum(choices=GIT_LAB_API_VERSION_CHOICES)
    connection_git_lab_hostname: str | None = create_generic_varchar()
    connection_git_lab_token: Secret | None = create_generic_fk(to=Secret)
    connection_git_lab_top_level_group_id: str | None = create_generic_varchar()
    connection_google_maps_api_key: Secret | None = create_generic_fk(to=Secret, related_name='server_config_google_maps')
    kpi_developers_to_exclude = create_generic_m2m(to='Person')
    scrum_capacity_base_per_day: float | None = create_generic_decimal()
    scrum_number_of_business_days_in_sprint: int | None = create_generic_integer()
    scrum_number_of_business_days_in_week: int | None = create_generic_integer()
    scrum_number_of_weeks_in_a_sprint: int | None = create_generic_integer()
    type_developer_role: Role | None = create_generic_fk(to=Role)

    @property
    def google_maps_api_key_decrypted(self) -> str | None:
        """Returns the decrypted Google Maps API key if configured, None otherwise."""
        if self.connection_google_maps_api_key:
            return self.connection_google_maps_api_key.get_encrypted_value()
        return None

    @property
    def coerced_scrum_capacity_base(self) -> int:
        if self.scrum_capacity_base is not None:
            return self.scrum_capacity_base
        return ceil(
            self.coerced_scrum_capacity_base_per_day
            * self.coerced_scrum_number_of_business_days_in_sprint
        )

    @property
    def coerced_scrum_capacity_base_per_day(self) -> float:
        return self.scrum_capacity_base_per_day or 2

    @property
    def coerced_scrum_number_of_business_days_in_sprint(self) -> int:
        if self.scrum_number_of_business_days_in_sprint is not None:
            return self.scrum_number_of_business_days_in_sprint
        return (
                self.coerced_scrum_number_of_business_days_in_week
                * self.coerced_scrum_number_of_weeks_in_a_sprint
        )

    @property
    def coerced_scrum_number_of_business_days_in_week(self) -> int:
        return self.scrum_number_of_business_days_in_week or 5

    @property
    def coerced_scrum_number_of_weeks_in_a_sprint(self) -> int:
        return self.scrum_number_of_weeks_in_a_sprint or 3

    @staticmethod
    def current() -> 'ThisServerConfiguration':
        return ThisServerConfiguration.objects.last() or ThisServerConfiguration.default()

    @staticmethod
    def default() -> 'ThisServerConfiguration':
        return ThisServerConfiguration(
            connection_git_lab_api_version=GIT_LAB_API_VERSION_FOUR,
            connection_git_lab_group_id=None,
            connection_git_lab_hostname="gitlab.com",
            connection_git_lab_token=None,
            scrum_capacity_base=30,
            scrum_capacity_base_per_day=2,
            scrum_number_of_business_days_in_sprint=15,
            scrum_number_of_business_days_in_week=5,
            scrum_number_of_weeks_in_a_sprint=3,
            type_developer_role=None,
        )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = "This Server Configuration"
        verbose_name_plural = "These Server Configurations"
