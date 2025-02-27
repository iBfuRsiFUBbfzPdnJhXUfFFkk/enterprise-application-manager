from django import forms
import json

from django.forms import CharField


class StringListField(CharField):
    def to_python(self, value):
        """Convert the input value to a Python list of strings."""
        value = super().to_python(value)
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            raise forms.ValidationError("This field should contain a valid JSON list.")

    def prepare_value(self, value):
        """Convert the Python list of strings to a JSON string."""
        if isinstance(value, list):
            return json.dumps(value)
        return value
