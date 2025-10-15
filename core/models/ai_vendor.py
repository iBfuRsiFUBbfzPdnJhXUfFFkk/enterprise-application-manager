from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class AIVendor(AbstractBaseModel, AbstractComment, AbstractName):
    """
    AI vendor/provider information (e.g., OpenAI, Anthropic, Google, etc.)
    """

    website_url = create_generic_varchar()
    contact_email = create_generic_varchar()
    support_url = create_generic_varchar()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'AI Vendor'
        verbose_name_plural = 'AI Vendors'
