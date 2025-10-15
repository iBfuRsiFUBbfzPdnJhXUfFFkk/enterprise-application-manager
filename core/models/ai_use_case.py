from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class AIUseCase(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Specific use case for AI within an application's AI governance.
    Multiple use cases can exist per AI governance record.
    """

    # Link to AI Governance
    ai_governance = create_generic_fk(to='AIGovernance', related_name='use_cases')

    # Use case details
    explanation = create_generic_varchar()
    purpose = create_generic_varchar()
    expected_benefit = create_generic_varchar()

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

    # Risk and monitoring
    risk_level = create_generic_varchar()
    monitoring_approach = create_generic_varchar()
    human_oversight_required = create_generic_boolean()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'AI Use Case'
        verbose_name_plural = 'AI Use Cases'
