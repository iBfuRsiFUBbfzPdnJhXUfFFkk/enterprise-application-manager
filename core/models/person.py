from core.models.common.abstract.comment import Comment
from core.models.common.enums.job_level_choices import JOB_LEVEL_CHOICES
from core.models.common.enums.job_title_choices import JOB_TITLE_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Person(Comment):
    is_active = create_generic_boolean(default=True)
    is_employee = create_generic_boolean(default=True)
    job_level = create_generic_enum(choices=JOB_LEVEL_CHOICES)
    job_title = create_generic_enum(choices=JOB_TITLE_CHOICES)
    link_gitlab_username = create_generic_varchar()
    name_first = create_generic_varchar()
    name_last = create_generic_varchar()

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.job_level} {self.job_title}"

    class Meta:
        verbose_name_plural = "People"
