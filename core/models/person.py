from core.models.common.comment import Comment
from core.models.common.create_generic_boolean import create_generic_boolean
from core.models.common.create_generic_enum import create_generic_enum
from core.models.common.create_generic_varchar import create_generic_varchar


class Person(Comment):
    JOB_LEVEL_JUNIOR = "Junior"
    JOB_LEVEL_MID_LEVEL = "Mid-Level"
    JOB_LEVEL_SENIOR = "Senior"

    JOB_TITLE_DEVELOPER = "Developer"
    JOB_TITLE_LEAD_DEVELOPER = "Lead Developer"
    JOB_TITLE_LEAD_SOFTWARE_ARCHITECT = "Lead Software Architect"
    JOB_TITLE_MANAGER = "Manager"
    JOB_TITLE_PRODUCT_MANAGER = "Product Manager"
    JOB_TITLE_PRODUCT_OWNER = "Product Owner"
    JOB_TITLE_PROJECT_MANAGER = "Project Manager"
    JOB_TITLE_SCRUM_MASTER = "Scrum Master"
    JOB_TITLE_SOFTWARE_ARCHITECT = "Software Architect"
    JOB_TITLE_SOFTWARE_SUPPORT_SPECIALIST = "Software Support Specialist"

    JOB_LEVEL_CHOICES = [
        (JOB_LEVEL_JUNIOR, JOB_LEVEL_JUNIOR),
        (JOB_LEVEL_MID_LEVEL, JOB_LEVEL_MID_LEVEL),
        (JOB_LEVEL_SENIOR, JOB_LEVEL_SENIOR),
    ]
    JOB_TITLE_CHOICES = [
        (JOB_TITLE_DEVELOPER, JOB_TITLE_DEVELOPER),
        (JOB_TITLE_LEAD_DEVELOPER, JOB_TITLE_LEAD_DEVELOPER),
        (JOB_TITLE_LEAD_SOFTWARE_ARCHITECT, JOB_TITLE_LEAD_SOFTWARE_ARCHITECT),
        (JOB_TITLE_MANAGER, JOB_TITLE_MANAGER),
        (JOB_TITLE_PRODUCT_MANAGER, JOB_TITLE_PRODUCT_MANAGER),
        (JOB_TITLE_PRODUCT_OWNER, JOB_TITLE_PRODUCT_OWNER),
        (JOB_TITLE_PROJECT_MANAGER, JOB_TITLE_PROJECT_MANAGER),
        (JOB_TITLE_SCRUM_MASTER, JOB_TITLE_SCRUM_MASTER),
        (JOB_TITLE_SOFTWARE_ARCHITECT, JOB_TITLE_SOFTWARE_ARCHITECT),
        (JOB_TITLE_SOFTWARE_SUPPORT_SPECIALIST, JOB_TITLE_SOFTWARE_SUPPORT_SPECIALIST),
    ]

    is_active = create_generic_boolean(default=True)
    is_employee = create_generic_boolean(default=True)
    job_level = create_generic_enum(choices=JOB_LEVEL_CHOICES)
    job_title = create_generic_enum(choices=JOB_TITLE_CHOICES)
    link_gitlab_username = create_generic_varchar()
    name_first = create_generic_varchar()
    name_last = create_generic_varchar()

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.job_level} {self.job_title}"
