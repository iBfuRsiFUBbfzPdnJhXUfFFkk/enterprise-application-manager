from django.forms import ModelForm

from core.models.database import Database


class DatabaseForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Database

    def save(self, commit=True):
        encrypted_password: str = self.cleaned_data['encrypted_password']
        encrypted_username: str = self.cleaned_data['encrypted_username']

        instance: Database = super().save(commit=False)
        instance.set_encrypted_password(secret=encrypted_password)
        instance.set_encrypted_username(secret=encrypted_username)
        if commit:
            instance.save()
        return instance
