from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

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
    application = create_generic_fk(to='Application', related_name='ai_governance')

    # Vendor information
    ai_vendor = create_generic_fk(to='AIVendor', related_name='ai_governance_records')

    # Approval information
    approval_status = create_generic_enum(choices=SIGN_OFF_CHOICES)
    approved_by = create_generic_fk(to='Person', related_name='ai_governance_approvals')
    approval_date = create_generic_date()

    # Contract and legal
    contract_number = create_generic_varchar()
    contract_url = create_generic_varchar()
    terms_of_service_url = create_generic_varchar()
    terms_of_use_url = create_generic_varchar()
    privacy_policy_url = create_generic_varchar()

    # Supporting documents
    supporting_document = create_generic_fk(to='Document', related_name='ai_governance_supporting')

    # Data protection and training
    data_protection_measures = create_generic_varchar()
    data_used_for_training = create_generic_boolean()
    data_retention_policy = create_generic_varchar()

    # Compliance
    compliance_framework = create_generic_varchar()
    risk_assessment_completed = create_generic_boolean()
    risk_assessment_date = create_generic_date()

    def __str__(self):
        if self.application:
            return f"AI Governance - {self.application.name}"
        return f"AI Governance #{self.id}"

    class Meta:
        ordering = ['-approval_date', '-id']
        verbose_name = 'AI Governance'
        verbose_name_plural = 'AI Governance Records'
