from django.db import models

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
    ai_use_case = models.ForeignKey('AIUseCase', on_delete=models.SET_NULL, null=True, blank=True, related_name='hallucinations')

    # Incident details
    incident_date = models.DateField(null=True, blank=True)
    severity = models.CharField(max_length=255, choices=HALLUCINATION_SEVERITY_CHOICES, null=True, blank=True)

    # Description
    hallucination_description = models.CharField(max_length=255, null=True, blank=True)
    expected_output = models.CharField(max_length=255, null=True, blank=True)
    actual_output = models.CharField(max_length=255, null=True, blank=True)

    # Context
    user_prompt = models.CharField(max_length=255, null=True, blank=True)
    context_information = models.CharField(max_length=255, null=True, blank=True)

    # Impact
    impact_description = models.CharField(max_length=255, null=True, blank=True)
    users_affected_count = models.CharField(max_length=255, null=True, blank=True)
    business_impact = models.CharField(max_length=255, null=True, blank=True)

    # Response and resolution
    reported_by = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_hallucinations_reported')
    resolution_description = models.CharField(max_length=255, null=True, blank=True)
    corrective_actions = models.CharField(max_length=255, null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    # Documentation
    supporting_document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_hallucination_documentation')
    incident_ticket_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.severity}"

    class Meta:
        ordering = ['-incident_date', '-severity', '-id']
        verbose_name = 'AI Hallucination'
        verbose_name_plural = 'AI Hallucinations'
