from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_text import create_generic_text
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class AIUseCase(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Specific use case for AI within an application's AI governance.
    Multiple use cases can exist per AI governance record.
    """

    # Link to AI Governance and Client
    ai_governance = create_generic_fk(to='AIGovernance', related_name='use_cases')
    client = create_generic_fk(to='Client', related_name='ai_use_cases')

    # Use case details
    explanation = create_generic_varchar()
    summary = create_generic_text()
    purpose = create_generic_varchar()
    expected_benefit = create_generic_varchar()
    intended_purpose_and_benefits = create_generic_text()
    is_currently_active = create_generic_boolean()
    development_lifecycle_stage = create_generic_varchar()
    use_case_topic_area = create_generic_varchar()

    # Face recognition/capture technology
    uses_face_recognition_or_capture = create_generic_boolean()

    # Commercial AI products
    is_in_commercial_ai_products_list = create_generic_boolean()

    # AI System outputs
    ai_system_outputs_description = create_generic_text()

    # Data involved
    data_description = create_generic_varchar()
    data_sources = create_generic_varchar()
    data_sensitivity_level = create_generic_varchar()
    personal_data_involved = create_generic_boolean()

    # Systems involved
    systems_description = create_generic_varchar()
    applications_involved = create_generic_m2m(to='Application')
    databases_involved = create_generic_m2m(to='Database')
    tools_involved = create_generic_m2m(to='Tool')

    # Data protection
    data_protection_measures = create_generic_varchar()
    encryption_used = create_generic_boolean()
    access_controls = create_generic_varchar()

    # Training and usage
    data_used_for_ai_training = create_generic_boolean()
    training_data_opt_out_available = create_generic_boolean()
    model_version = create_generic_varchar()
    agency_owned_training_data_description = create_generic_text()
    has_model_training_data_documentation = create_generic_boolean()
    demographic_variables_used = create_generic_text()

    # Development and code
    includes_custom_developed_code = create_generic_boolean()
    agency_has_code_access = create_generic_boolean()
    open_source_code_url = create_generic_varchar()
    developed_under_contract_or_inhouse = create_generic_varchar()
    procurement_instrument_identifiers = create_generic_text()

    # Authority to Operate
    has_ato_for_ai_system = create_generic_boolean()
    ato_system_name = create_generic_varchar()

    # Risk and monitoring
    risk_level = create_generic_varchar()
    monitoring_approach = create_generic_varchar()
    human_oversight_required = create_generic_boolean()
    is_rights_impacting = create_generic_boolean()
    presumed_rights_impacting_category = create_generic_varchar()
    is_safety_impacting = create_generic_boolean()
    presumed_safety_impacting_category = create_generic_varchar()
    caio_determination_justification = create_generic_text()
    key_risks_and_identification_method = create_generic_text()

    # Dates
    date_initiated = create_generic_date()
    date_development_or_acquisition_began = create_generic_date()
    date_deployed = create_generic_date()
    date_retired = create_generic_date()

    # HISP and public-facing services
    supports_hisp_public_facing_service = create_generic_boolean()
    hisp_supporting = create_generic_varchar()
    public_facing_service_supporting = create_generic_varchar()
    disseminates_info_to_public = create_generic_boolean()
    info_quality_act_compliance_approach = create_generic_text()

    # Privacy and PII
    involves_pii_maintained_by_client = create_generic_boolean()
    saop_assessed_privacy_risks = create_generic_boolean()

    # Data and infrastructure access
    has_access_to_enterprise_data_catalog = create_generic_varchar()
    wait_time_for_developer_tools = create_generic_varchar()
    it_infrastructure_provisioning_method = create_generic_text()
    has_computing_resources_request_process = create_generic_text()
    is_provisioning_communication_timely = create_generic_text()
    data_science_tools_reuse_approach = create_generic_text()

    # Review and assessment
    info_made_available_for_review = create_generic_boolean()
    requested_extension_for_risk_management = create_generic_boolean()
    ai_impact_assessment_conducted = create_generic_boolean()
    tested_in_operational_environment = create_generic_boolean()
    independent_evaluation_conducted = create_generic_boolean()
    has_post_deployment_monitoring_process = create_generic_boolean()

    # Decision-making and human involvement
    can_ai_act_without_human_involvement = create_generic_boolean()
    ai_use_notice_approach = create_generic_text()

    # Fairness and equity
    disparities_detection_mitigation_steps = create_generic_text()
    is_used_for_decisions_with_adverse_impact = create_generic_boolean()
    affected_groups_consultation_steps = create_generic_text()

    # Fallback and opt-out
    has_fallback_and_escalation_process = create_generic_text()
    has_opt_out_mechanism = create_generic_text()

    # Contact information
    contact_name = create_generic_varchar()
    contact_email = create_generic_varchar()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'AI Use Case'
        verbose_name_plural = 'AI Use Cases'
