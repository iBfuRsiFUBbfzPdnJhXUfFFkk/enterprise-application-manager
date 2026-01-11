from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import (
    create_generic_integer,
)
from django_generic_model_fields.create_generic_varchar import (
    create_generic_varchar,
)


class APIRequestExecution(AbstractBaseModel):
    _disable_history = True  # High-volume operational log with large JSON payloads

    api_request = create_generic_fk(to='APIRequest', related_name='executions')
    executed_by = create_generic_fk(to='Person', related_name='api_executions')
    executed_at = models.DateTimeField(auto_now_add=True)
    environment = create_generic_varchar()
    executed_url = models.TextField()

    executed_path_parameters = models.JSONField(blank=True, null=True)
    executed_query_parameters = models.JSONField(blank=True, null=True)
    executed_headers = models.JSONField(blank=True, null=True)
    executed_body = models.TextField(blank=True, null=True)

    response_status_code = create_generic_integer()
    response_headers = models.JSONField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    response_time_ms = create_generic_integer()

    is_error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        request_name = (
            self.api_request.name if self.api_request else 'Unknown Request'
        )
        status = (
            f"{self.response_status_code}"
            if self.response_status_code
            else "Error"
        )
        return f"{request_name} - {status} - {self.executed_at}"

    class Meta:
        ordering = ['-executed_at', '-id']
        verbose_name = "API Request Execution"
        verbose_name_plural = "API Request Executions"
