from django.db import models

from core.models.application_group import ApplicationGroup
from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_commentable import AbstractCommentable
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.authentication_choices import AUTHENTICATION_TYPE_CHOICES
from core.models.common.enums.authorization_choices import AUTHORIZATION_TYPE_CHOICES
from core.models.common.enums.centralized_logging_status_choices import (
    CENTRALIZED_LOGGING_STATUS_CHOICES,
)
from core.models.common.enums.deployment_medium_choices import DEPLOYMENT_MEDIUM_CHOICES
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from core.models.common.enums.pipeline_status_choices import PIPELINE_STATUS_CHOICES
from core.models.common.enums.platform_target_choices import PLATFORM_TARGET_CHOICES
from core.models.document import Document
from core.models.link import Link
from core.models.person import Person
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool
from core.utilities.get_name_acronym import get_name_acronym


class Application(AbstractAlias, AbstractAcronym, AbstractBaseModel, AbstractComment, AbstractCommentable, AbstractName):
    application_downstream_dependencies = models.ManyToManyField('self', blank=True, related_name='upstream_dependent_applications', symmetrical=False)
    application_group_platform = models.ForeignKey(ApplicationGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    application_groups = models.ManyToManyField(ApplicationGroup, blank=True, related_name='grouped_applications')
    application_upstream_dependencies = models.ManyToManyField('self', blank=True, related_name='downstream_dependent_applications', symmetrical=False)
    date_launch = models.DateField(null=True, blank=True)
    is_externally_facing = models.BooleanField(null=True, blank=True)
    is_legacy = models.BooleanField(null=True, blank=True)
    is_required_to_adhere_to_california_consumer_privacy_act_ccpa = models.BooleanField(null=True, blank=True)
    is_required_to_adhere_to_general_data_protection_regulation_gdpr = models.BooleanField(null=True, blank=True)
    is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss = models.BooleanField(null=True, blank=True)
    is_storing_nonpublic_personal_information_npi = models.BooleanField(null=True, blank=True)
    is_storing_personally_identifiable_information_pii = models.BooleanField(null=True, blank=True)
    is_storing_protected_health_information_phi = models.BooleanField(null=True, blank=True)
    is_using_artificial_intelligence = models.BooleanField(null=True, blank=True)
    link_development_server = models.CharField(max_length=255, null=True, blank=True)
    link_divio = models.CharField(max_length=255, null=True, blank=True)
    link_gitlab_repository = models.CharField(max_length=255, null=True, blank=True)
    link_gitlab_wiki = models.CharField(max_length=255, null=True, blank=True)
    link_logs = models.CharField(max_length=255, null=True, blank=True)
    link_lucid = models.CharField(max_length=255, null=True, blank=True)
    link_open_ai = models.CharField(max_length=255, null=True, blank=True)
    link_postman = models.CharField(max_length=255, null=True, blank=True)
    link_production_server = models.CharField(max_length=255, null=True, blank=True)
    link_production_server_external = models.CharField(max_length=255, null=True, blank=True)
    link_sentry_io = models.CharField(max_length=255, null=True, blank=True)
    link_software_bill_of_materials_sbom = models.CharField(max_length=255, null=True, blank=True)
    link_staging_server = models.CharField(max_length=255, null=True, blank=True)
    link_support_email = models.CharField(max_length=255, null=True, blank=True)
    link_teams_channel = models.CharField(max_length=255, null=True, blank=True)
    link_training = models.CharField(max_length=255, null=True, blank=True)
    link_ticket_submission = models.CharField(max_length=255, null=True, blank=True)
    link_whiteboard = models.CharField(max_length=255, null=True, blank=True)
    link_wrike = models.CharField(max_length=255, null=True, blank=True)
    peak_userbase = models.IntegerField(null=True, blank=True)
    person_architect = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_architect')
    person_developers = models.ManyToManyField(Person, blank=True, related_name='applications_developer_of')
    person_lead_developer = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_lead_developer')
    person_product_manager = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_product_manager')
    person_product_owner = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_product_owner')
    person_project_manager = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_project_manager')
    person_scrum_master = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_as_scrum_master')
    person_smes = models.ManyToManyField(Person, blank=True, related_name='applications_sme_of')
    person_stakeholders = models.ManyToManyField(Person, blank=True, related_name='applications_stakeholder_of')
    service_providers = models.ManyToManyField(ServiceProvider, blank=True, related_name='applications_that_use_service_provider')
    tools = models.ManyToManyField(Tool, blank=True, related_name='applications_that_use_tool')
    links = models.ManyToManyField(Link, blank=True, related_name='applications')
    documents = models.ManyToManyField(Document, blank=True, related_name='applications')
    centralized_logging_status = models.CharField(max_length=255, choices=CENTRALIZED_LOGGING_STATUS_CHOICES, null=True, blank=True)
    pipeline_status = models.CharField(max_length=255, choices=PIPELINE_STATUS_CHOICES, null=True, blank=True)
    type_authentication = models.CharField(max_length=255, choices=AUTHENTICATION_TYPE_CHOICES, null=True, blank=True)
    type_authorization = models.CharField(max_length=255, choices=AUTHORIZATION_TYPE_CHOICES, null=True, blank=True)
    type_deployment_medium = models.CharField(max_length=255, choices=DEPLOYMENT_MEDIUM_CHOICES, null=True, blank=True)
    type_lifecycle = models.CharField(max_length=255, choices=LIFECYCLE_CHOICES, null=True, blank=True)
    type_platform_target = models.CharField(max_length=255, choices=PLATFORM_TARGET_CHOICES, null=True, blank=True)

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', 'acronym', '-id']
