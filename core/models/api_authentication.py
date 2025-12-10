from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.api_auth_type_choices import API_AUTH_TYPE_CHOICES
from core.models.common.enums.api_key_location_choices import (
    API_KEY_LOCATION_CHOICES,
)
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class APIAuthentication(AbstractBaseModel, AbstractComment, AbstractName):
    api = create_generic_fk(to='API', related_name='authentications')
    auth_type = create_generic_enum(choices=API_AUTH_TYPE_CHOICES)

    # API Key fields
    api_key_location = create_generic_enum(choices=API_KEY_LOCATION_CHOICES)
    api_key_name = create_generic_varchar()
    secret_api_key = create_generic_fk(
        to='Secret', related_name='api_auth_api_key'
    )

    # Bearer Token / OAuth fields
    secret_bearer_token = create_generic_fk(
        to='Secret', related_name='api_auth_bearer_token'
    )
    oauth_token_url = create_generic_varchar()
    oauth_client_id = create_generic_varchar()
    secret_oauth_client_secret = create_generic_fk(
        to='Secret', related_name='api_auth_oauth_secret'
    )

    # Basic Auth fields
    basic_auth_username = create_generic_varchar()
    secret_basic_auth_password = create_generic_fk(
        to='Secret', related_name='api_auth_basic_password'
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
