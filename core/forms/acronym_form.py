from django.forms import ModelForm

from core.models.acronym import Acronym


class AcronymForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Acronym
