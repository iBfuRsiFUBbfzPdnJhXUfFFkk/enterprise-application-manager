from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, ManyToManyField


class Display(Model):
    display_label = CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class Person(Display):
    JOB_LEVEL_JUNIOR = "Junior"
    JOB_LEVEL_MID_LEVEL = "Mid-Level"
    JOB_LEVEL_SENIOR = "Senior"

    JOB_TITLE_DEVELOPER = "Developer"
    JOB_TITLE_LEAD_DEVELOPER = "Lead Developer"
    JOB_TITLE_LEAD_SOFTWARE_ARCHITECT = "Lead Software Architect"
    JOB_TITLE_PRODUCT_MANAGER = "Product Manager"
    JOB_TITLE_PRODUCT_OWNER = "Product Owner"
    JOB_TITLE_PROJECT_MANAGER = "Project Manager"
    JOB_TITLE_SCRUM_MASTER = "Scrum Master"
    JOB_TITLE_SOFTWARE_ARCHITECT = "Software Architect"

    JOB_LEVEL_CHOICES = [
        (JOB_LEVEL_JUNIOR, JOB_LEVEL_JUNIOR),
        (JOB_LEVEL_MID_LEVEL, JOB_LEVEL_MID_LEVEL),
        (JOB_LEVEL_SENIOR, JOB_LEVEL_SENIOR),
    ]
    JOB_TITLE_CHOICES = [
        (JOB_TITLE_DEVELOPER, JOB_TITLE_DEVELOPER),
        (JOB_TITLE_LEAD_DEVELOPER, JOB_TITLE_LEAD_DEVELOPER),
        (JOB_TITLE_LEAD_SOFTWARE_ARCHITECT, JOB_TITLE_LEAD_SOFTWARE_ARCHITECT),
        (JOB_TITLE_PRODUCT_MANAGER, JOB_TITLE_PRODUCT_MANAGER),
        (JOB_TITLE_PRODUCT_OWNER, JOB_TITLE_PRODUCT_OWNER),
        (JOB_TITLE_PROJECT_MANAGER, JOB_TITLE_PROJECT_MANAGER),
        (JOB_TITLE_SCRUM_MASTER, JOB_TITLE_SCRUM_MASTER),
        (JOB_TITLE_SOFTWARE_ARCHITECT, JOB_TITLE_SOFTWARE_ARCHITECT),
    ]

    job_level = CharField(choices=JOB_LEVEL_CHOICES, max_length=25, null=True)
    job_title = CharField(choices=JOB_TITLE_CHOICES, max_length=25, null=True)
    link_gitlab_username = CharField(max_length=255, null=True)
    name_first = CharField(max_length=255, null=True)
    name_last = CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.job_level} {self.job_title}"


class Application(Display):
    acronym = CharField(max_length=255, null=True)
    person_architect = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_architect',
        "to": Person,
    })
    person_developers = ManyToManyField(**{
        "blank": True,
        "to": Person,
    })
    person_lead_developer = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_lead_developer',
        "to": Person,
    })
    person_product_manager = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_product_manager',
        "to": Person,
    })
    person_product_owner = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_product_owner',
        "to": Person,
    })
    person_project_manager = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_project_manager',
        "to": Person,
    })
    person_scrum_master = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_scrum_master',
        "to": Person,
    })

    def __str__(self):
        return f"{self.display_label} ({self.acronym})"
