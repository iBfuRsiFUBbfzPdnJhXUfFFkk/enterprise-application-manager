from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.enums.sign_off_choices import SIGN_OFF_CHOICES


class AIGovernance(AbstractBaseModel, AbstractComment):
    """
    AI Governance record for an application.
    One-to-one relationship with Application.
    Tracks overall AI usage approval, contracts, terms, and compliance.
    """

    # One-to-one relationship with Application
    application = models.ForeignKey('Application', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_governance')

    # Vendor information
    ai_vendor = models.ForeignKey('AIVendor', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_governance_records')

    # Approval information
    approval_status = models.CharField(max_length=255, choices=SIGN_OFF_CHOICES, null=True, blank=True)
    approved_by = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_governance_approvals')
    approval_date = models.DateField(null=True, blank=True)

    # Contract and legal
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    contract_url = models.CharField(max_length=255, null=True, blank=True)
    terms_of_service_url = models.CharField(max_length=255, null=True, blank=True)
    terms_of_use_url = models.CharField(max_length=255, null=True, blank=True)
    privacy_policy_url = models.CharField(max_length=255, null=True, blank=True)

    # Supporting documents
    supporting_document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_governance_supporting')

    # Data protection and training
    data_protection_measures = models.CharField(max_length=255, null=True, blank=True)
    data_used_for_training = models.BooleanField(null=True, blank=True)
    data_retention_policy = models.CharField(max_length=255, null=True, blank=True)

    # Compliance
    compliance_framework = models.CharField(max_length=255, null=True, blank=True)
    risk_assessment_completed = models.BooleanField(null=True, blank=True)
    risk_assessment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.application:
            return f"AI Governance - {self.application.name}"
        return f"AI Governance #{self.id}"

    class Meta:
        ordering = ['-approval_date', '-id']
        verbose_name = 'AI Governance'
        verbose_name_plural = 'AI Governance Records'
