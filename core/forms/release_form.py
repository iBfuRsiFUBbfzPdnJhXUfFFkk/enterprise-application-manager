from django.forms import ModelForm

from core.models.release import Release


class ReleaseForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Release
