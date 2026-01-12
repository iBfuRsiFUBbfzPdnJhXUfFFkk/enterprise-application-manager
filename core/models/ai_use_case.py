from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class AIUseCase(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Specific use case for AI within an application's AI governance.
    Multiple use cases can exist per AI governance record.
    """

    # Link to AI Governance
    ai_governance = models.ForeignKey('AIGovernance', on_delete=models.SET_NULL, null=True, blank=True, related_name='use_cases')

    # Use case details
    explanation = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.CharField(max_length=255, null=True, blank=True)
    expected_benefit = models.CharField(max_length=255, null=True, blank=True)

    # Data involved
    data_description = models.CharField(max_length=255, null=True, blank=True)
    data_sources = models.CharField(max_length=255, null=True, blank=True)
    data_sensitivity_level = models.CharField(max_length=255, null=True, blank=True)
    personal_data_involved = models.BooleanField(null=True, blank=True)

    # Systems involved
    systems_description = models.CharField(max_length=255, null=True, blank=True)
    applications_involved = models.ManyToManyField('Application', blank=True, related_name='ai_use_cases')
    databases_involved = models.ManyToManyField('Database', blank=True, related_name='ai_use_cases')
    tools_involved = models.ManyToManyField('Tool', blank=True, related_name='ai_use_cases')

    # Data protection
    data_protection_measures = models.CharField(max_length=255, null=True, blank=True)
    encryption_used = models.BooleanField(null=True, blank=True)
    access_controls = models.CharField(max_length=255, null=True, blank=True)

    # Training and usage
    data_used_for_ai_training = models.BooleanField(null=True, blank=True)
    training_data_opt_out_available = models.BooleanField(null=True, blank=True)
    model_version = models.CharField(max_length=255, null=True, blank=True)

    # Risk and monitoring
    risk_level = models.CharField(max_length=255, null=True, blank=True)
    monitoring_approach = models.CharField(max_length=255, null=True, blank=True)
    human_oversight_required = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'AI Use Case'
        verbose_name_plural = 'AI Use Cases'
