from django import forms
from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.api_request import APIRequest


class APIRequestForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = APIRequest
        widgets = {
            'path_parameters': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '{"id": {"type": "string", "default": "123"}}',
                }
            ),
            'query_parameters': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '{"page": {"type": "integer", "default": "1"}}',
                }
            ),
            'custom_headers': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '{"X-Custom-Header": "value"}',
                }
            ),
            'form_data': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '{"username": "john", "password": "secret"}',
                }
            ),
            'request_body': forms.Textarea(
                attrs={
                    'rows': 10,
                    'placeholder': 'Request body (JSON, XML, etc.)',
                }
            ),
        }
