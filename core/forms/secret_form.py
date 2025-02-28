from django.forms import ModelForm

from core.models.secret import Secret


class SecretForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Secret

    def save(self, commit=True):
        encrypted_value: str = self.cleaned_data['encrypted_value']

        instance: Secret = super().save(commit=False)
        instance.set_encrypted_value(secret=encrypted_value)
        if commit:
            instance.save()
        return instance
