from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.environment_choices import ENVIRONMENT_CHOICES
from core.models.common.enums.http_method_choices import HTTP_METHOD_CHOICES
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class APIRequest(AbstractBaseModel, AbstractComment, AbstractName):
    api = create_generic_fk(to='API', related_name='requests')
    authentication = create_generic_fk(
        to='APIAuthentication', related_name='requests'
    )

    http_method = create_generic_enum(choices=HTTP_METHOD_CHOICES)
    default_environment = create_generic_enum(choices=ENVIRONMENT_CHOICES)
    url_path = create_generic_varchar()

    path_parameters = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text='JSON object defining path parameters',
    )

    query_parameters = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text='JSON object defining query parameters',
    )

    custom_headers = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text='JSON object of custom headers',
    )

    form_data = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text='Form data key-value pairs for x-www-form-urlencoded requests',
    )

    request_body = models.TextField(
        blank=True,
        null=True,
        help_text='Request body (JSON, XML, or raw text)',
    )

    content_type = create_generic_varchar()

    def __str__(self):
        api_name = self.api.name if self.api else 'No API'
        method = self.http_method if self.http_method else 'NO_METHOD'
        path = self.url_path if self.url_path else '/'
        return f"{api_name} - {method} {path}"

    class Meta:
        ordering = ['api__name', 'http_method', 'url_path', '-id']
