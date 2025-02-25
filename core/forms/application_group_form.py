from django.forms import ModelForm

from core.models.application_group import ApplicationGroup


class ApplicationGroupForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = ApplicationGroup
