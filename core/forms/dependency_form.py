from django.forms import ModelForm

from core.models.dependency import Dependency


class DependencyForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Dependency
