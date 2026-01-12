from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.api_auth_type_choices import API_AUTH_TYPE_CHOICES
from core.models.common.enums.api_key_location_choices import (
    API_KEY_LOCATION_CHOICES,
)


class APIAuthentication(AbstractBaseModel, AbstractComment, AbstractName):
    api = models.ForeignKey('API', on_delete=models.SET_NULL, null=True, blank=True, related_name='authentications')
    auth_type = models.CharField(max_length=255, choices=API_AUTH_TYPE_CHOICES, null=True, blank=True)

    # API Key fields
    api_key_location = models.CharField(max_length=255, choices=API_KEY_LOCATION_CHOICES, null=True, blank=True)
    api_key_name = models.CharField(max_length=255, null=True, blank=True)
    secret_api_key = models.ForeignKey(
        'Secret',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='api_auth_api_key'
    )

    # Bearer Token / OAuth fields
    secret_bearer_token = models.ForeignKey(
        'Secret',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='api_auth_bearer_token'
    )
    oauth_token_url = models.CharField(max_length=255, null=True, blank=True)
    oauth_client_id = models.CharField(max_length=255, null=True, blank=True)
    secret_oauth_client_secret = models.ForeignKey(
        'Secret',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='api_auth_oauth_secret'
    )

    # Basic Auth fields
    basic_auth_username = models.CharField(max_length=255, null=True, blank=True)
    secret_basic_auth_password = models.ForeignKey(
        'Secret',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='api_auth_basic_password'
    )

    # Custom Headers (stored as JSON text)
    custom_headers = models.TextField(
        blank=True,
        null=True,
        help_text='JSON object of custom headers with encrypted values',
    )

    def __str__(self):
        auth_type_display = self.auth_type if self.auth_type else 'Unknown'
        api_name = self.api.name if self.api else 'No API'
        return f"{api_name} - {auth_type_display}"

    class Meta:
        ordering = ['api__name', 'auth_type', '-id']
