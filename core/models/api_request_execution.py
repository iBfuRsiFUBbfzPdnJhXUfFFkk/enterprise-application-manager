from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class APIRequestExecution(AbstractBaseModel):
    _disable_history = True  # High-volume operational log with large JSON payloads

    api_request = models.ForeignKey('APIRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='executions')
    executed_by = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='api_executions')
    executed_at = models.DateTimeField(auto_now_add=True)
    environment = models.CharField(max_length=255, null=True, blank=True)
    executed_url = models.TextField()

    executed_path_parameters = models.JSONField(blank=True, null=True)
    executed_query_parameters = models.JSONField(blank=True, null=True)
    executed_headers = models.JSONField(blank=True, null=True)
    executed_body = models.TextField(blank=True, null=True)

    response_status_code = models.IntegerField(null=True, blank=True)
    response_headers = models.JSONField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    response_time_ms = models.IntegerField(null=True, blank=True)

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
