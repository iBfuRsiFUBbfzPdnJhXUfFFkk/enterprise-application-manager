from core.models.common.abstract.acronym import Acronym
from core.models.application_group import ApplicationGroup
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.enums.authentication_choices import AUTHENTICATION_TYPE_CHOICES
from core.models.common.enums.authorization_choices import AUTHORIZATION_TYPE_CHOICES
from core.models.common.enums.deployment_medium_choices import DEPLOYMENT_MEDIUM_CHOICES
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from core.models.common.enums.platform_target_choices import PLATFORM_TARGET_CHOICES
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_m2m import create_generic_m2m
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.person import Person
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool
from core.utilities.get_name_acronym import get_name_acronym


class Application(Alias, Acronym, BaseModel, Comment, Name):
    application_downstream_dependencies = create_generic_m2m(to='self')
    application_group_platform = create_generic_fk(related_name='applications', to=ApplicationGroup)
    application_groups = create_generic_m2m(to=ApplicationGroup)
    application_upstream_dependencies = create_generic_m2m(to='self')
    date_launch = create_generic_date()
    is_externally_facing = create_generic_boolean()
    is_legacy = create_generic_boolean()
    is_required_to_adhere_to_california_consumer_privacy_act_ccpa = create_generic_boolean()
    is_required_to_adhere_to_general_data_protection_regulation_gdpr = create_generic_boolean()
    is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss = create_generic_boolean()
    is_storing_nonpublic_personal_information_npi = create_generic_boolean()
    is_storing_personally_identifiable_information_pii = create_generic_boolean()
    is_storing_protected_health_information_phi = create_generic_boolean()
    is_using_artificial_intelligence = create_generic_boolean()
    link_development_server = create_generic_varchar()
    link_divio = create_generic_varchar()
    link_gitlab_repository = create_generic_varchar()
    link_gitlab_wiki = create_generic_varchar()
    link_logs = create_generic_varchar()
    link_lucid = create_generic_varchar()
    link_open_ai = create_generic_varchar()
    link_postman = create_generic_varchar()
    link_production_server = create_generic_varchar()
    link_production_server_external = create_generic_varchar()
    link_sentry_io = create_generic_varchar()
    link_software_bill_of_materials_sbom = create_generic_varchar()
    link_staging_server = create_generic_varchar()
    link_support_email = create_generic_varchar()
    link_teams_channel = create_generic_varchar()
    link_training = create_generic_varchar()
    link_ticket_submission = create_generic_varchar()
    link_whiteboard = create_generic_varchar()
    link_wrike = create_generic_varchar()
    peak_userbase = create_generic_integer()
    person_architect = create_generic_fk(related_name='applications_as_architect', to=Person)
    person_developers = create_generic_m2m(related_name='applications_developer_of', to=Person)
    person_lead_developer = create_generic_fk(related_name='applications_as_lead_developer', to=Person)
    person_product_manager = create_generic_fk(related_name='applications_as_product_manager', to=Person)
    person_product_owner = create_generic_fk(related_name='applications_as_product_owner', to=Person)
    person_project_manager = create_generic_fk(related_name='applications_as_project_manager', to=Person)
    person_scrum_master = create_generic_fk(related_name='applications_as_scrum_master', to=Person)
    person_stakeholders = create_generic_m2m(related_name='applications_stakeholder_of', to=Person)
    service_providers = create_generic_m2m(related_name='applications_that_use_service_provider', to=ServiceProvider)
    tools = create_generic_m2m(related_name='applications_that_use_tool', to=Tool)
    type_authentication = create_generic_enum(choices=AUTHENTICATION_TYPE_CHOICES)
    type_authorization = create_generic_enum(choices=AUTHORIZATION_TYPE_CHOICES)
    type_deployment_medium = create_generic_enum(choices=DEPLOYMENT_MEDIUM_CHOICES)
    type_lifecycle = create_generic_enum(choices=LIFECYCLE_CHOICES)
    type_platform_target = create_generic_enum(choices=PLATFORM_TARGET_CHOICES)

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', 'acronym', '-id']
