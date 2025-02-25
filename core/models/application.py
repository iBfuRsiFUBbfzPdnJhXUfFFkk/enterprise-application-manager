from core.models.common.comment import Comment
from core.models.common.create_generic_boolean import create_generic_boolean
from core.models.common.create_generic_date import create_generic_date
from core.models.common.create_generic_enum import create_generic_enum
from core.models.common.create_generic_fk import create_generic_fk
from core.models.common.create_generic_integer import create_generic_integer
from core.models.common.create_generic_m2m import create_generic_m2m
from core.models.common.create_generic_varchar import create_generic_varchar
from core.models.person import Person


class Application(Comment):
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

    acronym = create_generic_varchar()
    application_downstream_dependencies = create_generic_m2m(to='self')
    application_name = create_generic_varchar()
    application_upstream_dependencies = create_generic_m2m(to='self')
    date_launch = create_generic_date()
    is_externally_facing = create_generic_boolean()
    link_development_server = create_generic_varchar()
    link_gitlab_repository = create_generic_varchar()
    link_production_server = create_generic_varchar()
    link_production_server_external = create_generic_varchar()
    link_staging_server = create_generic_varchar()
    peak_userbase = create_generic_integer()
    person_architect = create_generic_fk(related_name='applications_as_architect', to=Person)
    person_developers = create_generic_m2m(to=Person)
    person_lead_developer = create_generic_fk(related_name='applications_as_lead_developer', to=Person)
    person_product_manager = create_generic_fk(related_name='applications_as_product_manager', to=Person)
    person_product_owner = create_generic_fk(related_name='applications_as_product_owner', to=Person)
    person_project_manager = create_generic_fk(related_name='applications_as_project_manager', to=Person)
    person_scrum_master = create_generic_fk(related_name='applications_as_scrum_master', to=Person)
    type_authentication = create_generic_enum(choices=AUTHENTICATION_TYPE_CHOICES)
    type_authorization = create_generic_enum(choices=AUTHORIZATION_TYPE_CHOICES)
    type_deployment_medium = create_generic_enum(choices=DEPLOYMENT_MEDIUM_CHOICES)
    type_lifecycle = create_generic_enum(choices=LIFECYCLE_CHOICES)
    type_platform = create_generic_enum(choices=PLATFORM_CHOICES)

    def __str__(self):
        return f"{self.application_name} ({self.acronym})"
