from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.location import Location
from core.models.common.abstract.pronunciation import Pronunciation
from core.models.common.enums.job_level_choices import JOB_LEVEL_CHOICES
from core.models.common.enums.job_title_choices import JOB_TITLE_CHOICES
from core.models.common.enums.timezone_choices import TIMEZONE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.job_level import JobLevel
from core.models.role import Role
from core.models.skill import Skill


class Person(BaseModel, Comment, Location, Pronunciation):
    date_birthday = create_generic_date()
    date_hired = create_generic_date()
    date_left = create_generic_date()
    gitlab_sync_access_level = create_generic_varchar()
    gitlab_sync_avatar_url = create_generic_varchar()
    gitlab_sync_datetime_created_at = create_generic_datetime()
    gitlab_sync_datetime_expires_at = create_generic_datetime()
    gitlab_sync_id = create_generic_varchar()
    gitlab_sync_is_locked = create_generic_boolean()
    gitlab_sync_membership_state = create_generic_varchar()
    gitlab_sync_name = create_generic_varchar()
    gitlab_sync_state = create_generic_varchar()
    gitlab_sync_username = create_generic_varchar()
    gitlab_sync_web_url = create_generic_varchar()
    is_active = create_generic_boolean(default=True)
    is_architect = create_generic_boolean()
    is_bot = create_generic_boolean()
    is_developer = create_generic_boolean()
    is_employee = create_generic_boolean(default=True)
    is_lead_developer = create_generic_boolean()
    is_product_manager = create_generic_boolean()
    is_product_owner = create_generic_boolean()
    is_project_manager = create_generic_boolean()
    is_scrum_master = create_generic_boolean()
    is_stakeholder = create_generic_boolean()
    link_sharepoint_profile = create_generic_varchar()
    job_level = create_generic_fk(related_name='people_who_hold_this_job_level', to=JobLevel)
    name_first = create_generic_varchar()
    name_last = create_generic_varchar()
    name_preferred = create_generic_varchar()
    roles = create_generic_m2m(related_name='people_who_hold_this_role', to=Role)
    scrum_capacity_base = create_generic_integer()
    skills = create_generic_m2m(related_name='people_who_hold_this_skill', to=Skill)
    type_job_level = create_generic_enum(choices=JOB_LEVEL_CHOICES)
    type_job_title = create_generic_enum(choices=JOB_TITLE_CHOICES)
    type_timezone = create_generic_enum(choices=TIMEZONE_CHOICES)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.type_job_level} {self.type_job_title}"

    class Meta:
        ordering = ['name_last', 'name_first', 'id']
        verbose_name_plural = "people"
