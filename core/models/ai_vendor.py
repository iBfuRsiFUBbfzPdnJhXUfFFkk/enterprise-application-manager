from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class AIVendor(AbstractBaseModel, AbstractComment, AbstractName):
    """
    AI vendor/provider information (e.g., OpenAI, Anthropic, Google, etc.)
    """

    website_url = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    support_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'AI Vendor'
        verbose_name_plural = 'AI Vendors'
