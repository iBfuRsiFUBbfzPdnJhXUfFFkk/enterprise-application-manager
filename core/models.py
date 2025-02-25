from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, ManyToManyField, BooleanField
from django.db.models.fields import DateField, IntegerField


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

    job_level = CharField(blank=True, choices=JOB_LEVEL_CHOICES, max_length=25, null=True)
    job_title = CharField(blank=True, choices=JOB_TITLE_CHOICES, max_length=25, null=True)
    link_gitlab_username = CharField(blank=True, max_length=255, null=True)
    name_first = CharField(blank=True, max_length=255, null=True)
    name_last = CharField(blank=True, max_length=255, null=True)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.job_level} {self.job_title}"


class Application(Display):
    PLATFORM_BACKGROUND_TASK = "Background Task"
    PLATFORM_CHROME_PLUGIN = "Chrome Plugin"
    PLATFORM_IOS = "IOS"
    PLATFORM_MICROSOFT_EXCEL = "Microsoft Excel"
    PLATFORM_MICROSOFT_EXCEL_VBA = "Microsoft Excel + Visual Basic for Applications"
    PLATFORM_MICROSOFT_WORD = "Microsoft Word"
    PLATFORM_WEB = "WEB"

    LIFECYCLE_ACTIVE = "Active"
    LIFECYCLE_APPROVAL = "Awaiting Approval"
    LIFECYCLE_DEPRECATED = "Deprecated"
    LIFECYCLE_DEVELOPMENT = "In Development"
    LIFECYCLE_HYPER_CARE = "Hyper Care"
    LIFECYCLE_IDEA = "Idea Submission"
    LIFECYCLE_IN_DEPRECATION = "In Deprecation Period"
    LIFECYCLE_LIMITED_SUPPORT = "Limited Support"
    LIFECYCLE_PLANNING = "In Planning"
    LIFECYCLE_REJECTED = "Approval Rejected"

    DEPLOYMENT_MEDIUM_CLOUD_AKS = "Cloud - Azure Kubernetes Service (AKS)"
    DEPLOYMENT_MEDIUM_CLOUD_DIVIO = "Cloud - Divio"
    DEPLOYMENT_MEDIUM_ON_PREMISES_IIS = "On-Premises - Windows Internet Information Services (IIS)"
    DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX = "On-Premises - Debian Linux"

    AUTHENTICATION_TYPE_AD = "Active Directory (AD)"
    AUTHENTICATION_TYPE_CUSTOM = "Custom"

    AUTHORIZATION_TYPE_AD = "Active Directory (AD)"
    AUTHORIZATION_TYPE_CUSTOM = "Custom"

    AUTHORIZATION_TYPE_CHOICES = [
        (AUTHORIZATION_TYPE_AD, AUTHORIZATION_TYPE_AD),
        (AUTHORIZATION_TYPE_CUSTOM, AUTHORIZATION_TYPE_CUSTOM),
    ]
    AUTHENTICATION_TYPE_CHOICES = [
        (AUTHENTICATION_TYPE_AD, AUTHENTICATION_TYPE_AD),
        (AUTHORIZATION_TYPE_CUSTOM, AUTHORIZATION_TYPE_CUSTOM),
    ]
    DEPLOYMENT_MEDIUM_CHOICES = [
        (DEPLOYMENT_MEDIUM_CLOUD_AKS, DEPLOYMENT_MEDIUM_CLOUD_AKS),
        (DEPLOYMENT_MEDIUM_CLOUD_DIVIO, DEPLOYMENT_MEDIUM_CLOUD_DIVIO),
        (DEPLOYMENT_MEDIUM_ON_PREMISES_IIS, DEPLOYMENT_MEDIUM_ON_PREMISES_IIS),
        (DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX, DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX),
    ]
    PLATFORM_CHOICES = [
        (PLATFORM_BACKGROUND_TASK, PLATFORM_BACKGROUND_TASK),
        (PLATFORM_CHROME_PLUGIN, PLATFORM_CHROME_PLUGIN),
        (PLATFORM_IOS, PLATFORM_IOS),
        (PLATFORM_MICROSOFT_EXCEL, PLATFORM_MICROSOFT_EXCEL),
        (PLATFORM_MICROSOFT_EXCEL_VBA, PLATFORM_MICROSOFT_EXCEL_VBA),
        (PLATFORM_MICROSOFT_WORD, PLATFORM_MICROSOFT_WORD),
        (PLATFORM_WEB, PLATFORM_WEB),
    ]
    LIFECYCLE_CHOICES = [
        (LIFECYCLE_ACTIVE, LIFECYCLE_ACTIVE),
        (LIFECYCLE_APPROVAL, LIFECYCLE_APPROVAL),
        (LIFECYCLE_DEPRECATED, LIFECYCLE_DEPRECATED),
        (LIFECYCLE_DEVELOPMENT, LIFECYCLE_DEVELOPMENT),
        (LIFECYCLE_HYPER_CARE, LIFECYCLE_HYPER_CARE),
        (LIFECYCLE_IDEA, LIFECYCLE_IDEA),
        (LIFECYCLE_IN_DEPRECATION, LIFECYCLE_IN_DEPRECATION),
        (LIFECYCLE_LIMITED_SUPPORT, LIFECYCLE_LIMITED_SUPPORT),
        (LIFECYCLE_PLANNING, LIFECYCLE_PLANNING),
        (LIFECYCLE_REJECTED, LIFECYCLE_REJECTED),
    ]

    acronym = CharField(blank=True, max_length=255, null=True)
    application_downstream_dependencies = ManyToManyField(**{
        "blank": True,
        "to": 'self',
    })
    application_upstream_dependencies = ManyToManyField(**{
        "blank": True,
        "to": 'self',
    })
    date_launch = DateField(blank=True, null=True)
    is_externally_facing = BooleanField(blank=True, default=False, null=True)
    link_development_server = CharField(blank=True, max_length=255, null=True)
    link_staging_server = CharField(blank=True, max_length=255, null=True)
    link_production_server = CharField(blank=True, max_length=255, null=True)
    link_production_server_external = CharField(blank=True, max_length=255, null=True)
    link_gitlab_repository = CharField(blank=True, max_length=255, null=True)
    peak_userbase = IntegerField(blank=True, null=True)
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
    type_authorization = CharField(blank=True, choices=AUTHORIZATION_TYPE_CHOICES, max_length=255, null=True)
    type_authentication = CharField(blank=True, choices=AUTHENTICATION_TYPE_CHOICES, max_length=255, null=True)
    type_deployment_medium = CharField(blank=True, choices=DEPLOYMENT_MEDIUM_CHOICES, max_length=255, null=True)
    type_lifecycle = CharField(blank=True, choices=LIFECYCLE_CHOICES, max_length=255, null=True)
    type_platform = CharField(blank=True, choices=PLATFORM_CHOICES, max_length=255, null=True)

    def __str__(self):
        return f"{self.display_label} ({self.acronym})"
