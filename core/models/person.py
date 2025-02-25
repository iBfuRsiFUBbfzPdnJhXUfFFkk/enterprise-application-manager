from core.models.common.abstract.comment import Comment
from core.models.common.enums.job_level_choices import JOB_LEVEL_CHOICES
from core.models.common.enums.job_title_choices import JOB_TITLE_CHOICES
from core.models.common.enums.timezone_choices import TIMEZONE_CHOICES
from core.models.common.enums.us_state_choices import US_STATE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Person(Comment):
    date_birthday = create_generic_date()
    date_hired = create_generic_date()
    date_left = create_generic_date()
    is_active = create_generic_boolean(default=True)
    is_architect = create_generic_boolean()
    is_developer = create_generic_boolean()
    is_employee = create_generic_boolean(default=True)
    is_lead_developer = create_generic_boolean()
    is_product_manager = create_generic_boolean()
    is_product_owner = create_generic_boolean()
    is_project_manager = create_generic_boolean()
    is_scrum_master = create_generic_boolean()
    is_stakeholder = create_generic_boolean()
    link_gitlab_username = create_generic_varchar()
    link_sharepoint_profile = create_generic_varchar()
    location_city = create_generic_varchar()
    location_state_code = create_generic_enum(choices=US_STATE_CHOICES)
    name_first = create_generic_varchar()
    name_last = create_generic_varchar()
    name_preferred = create_generic_varchar()
    name_pronunciation = create_generic_varchar()
    type_job_level = create_generic_enum(choices=JOB_LEVEL_CHOICES)
    type_job_title = create_generic_enum(choices=JOB_TITLE_CHOICES)
    type_timezone = create_generic_enum(choices=TIMEZONE_CHOICES)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.type_job_level} {self.type_job_title}"

    class Meta:
        verbose_name_plural = "People"
