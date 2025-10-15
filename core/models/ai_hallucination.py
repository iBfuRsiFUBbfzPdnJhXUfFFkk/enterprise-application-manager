from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName

# Severity choices for hallucination incidents
HALLUCINATION_SEVERITY_CRITICAL = "Critical"
HALLUCINATION_SEVERITY_HIGH = "High"
HALLUCINATION_SEVERITY_MEDIUM = "Medium"
HALLUCINATION_SEVERITY_LOW = "Low"

HALLUCINATION_SEVERITY_CHOICES = [
    (HALLUCINATION_SEVERITY_CRITICAL, HALLUCINATION_SEVERITY_CRITICAL),
    (HALLUCINATION_SEVERITY_HIGH, HALLUCINATION_SEVERITY_HIGH),
    (HALLUCINATION_SEVERITY_MEDIUM, HALLUCINATION_SEVERITY_MEDIUM),
    (HALLUCINATION_SEVERITY_LOW, HALLUCINATION_SEVERITY_LOW),
]


class AIHallucination(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Record of AI hallucination incidents for a specific use case.
    Tracks when the AI provided incorrect, fabricated, or misleading information.
    """

    # Link to AI Use Case
    ai_use_case = create_generic_fk(to='AIUseCase', related_name='hallucinations')

    # Incident details
    incident_date = create_generic_date()
    severity = create_generic_enum(choices=HALLUCINATION_SEVERITY_CHOICES)

    # Description
    hallucination_description = create_generic_varchar()
    expected_output = create_generic_varchar()
    actual_output = create_generic_varchar()

    # Context
    user_prompt = create_generic_varchar()
    context_information = create_generic_varchar()

    # Impact
    impact_description = create_generic_varchar()
    users_affected_count = create_generic_varchar()
    business_impact = create_generic_varchar()

    # Response and resolution
    reported_by = create_generic_fk(to='Person', related_name='ai_hallucinations_reported')
    resolution_description = create_generic_varchar()
    corrective_actions = create_generic_varchar()
    resolved_date = create_generic_date()

    # Documentation
    supporting_document = create_generic_fk(to='Document', related_name='ai_hallucination_documentation')
    incident_ticket_url = create_generic_varchar()

    def __str__(self):
        return f"{self.name} - {self.severity}"

    class Meta:
        ordering = ['-incident_date', '-severity', '-id']
        verbose_name = 'AI Hallucination'
        verbose_name_plural = 'AI Hallucinations'
