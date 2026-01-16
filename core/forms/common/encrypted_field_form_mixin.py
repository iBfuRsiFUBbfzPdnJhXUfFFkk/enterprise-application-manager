"""
Mixin for forms with encrypted fields to prevent displaying encrypted values.

This mixin clears the initial values of encrypted fields when editing existing
instances, preventing encrypted strings from being displayed in form fields.
"""


class EncryptedFieldFormMixin:
    """
    Mixin to clear encrypted field initial values when editing.

    Usage:
        class MyForm(EncryptedFieldFormMixin, BaseModelForm):
            encrypted_field_names = ['encrypted_password', 'encrypted_username']

            class Meta:
                model = MyModel
                fields = '__all__'

    Attributes:
        encrypted_field_names: List of field names to clear when editing
    """

    encrypted_field_names: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only clear fields when editing (instance exists)
        if self.instance and self.instance.pk:
            for field_name in self.encrypted_field_names:
                if field_name in self.fields:
                    # Clear the initial value in both places
                    self.fields[field_name].initial = None
                    self.initial[field_name] = None
                    # Add helpful placeholder text
                    self.fields[field_name].widget.attrs['placeholder'] = 'Leave blank to keep existing value'
