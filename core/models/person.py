from django.db.models import CharField, BooleanField

from core.models.common.comment import Comment


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

    is_active = BooleanField(blank=True, default=True, null=True)
    is_employee = BooleanField(blank=True, default=True, null=True)
    job_level = CharField(blank=True, choices=JOB_LEVEL_CHOICES, max_length=255, null=True)
    job_title = CharField(blank=True, choices=JOB_TITLE_CHOICES, max_length=255, null=True)
    link_gitlab_username = CharField(blank=True, max_length=255, null=True)
    name_first = CharField(blank=True, max_length=255, null=True)
    name_last = CharField(blank=True, max_length=255, null=True)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.job_level} {self.job_title}"
