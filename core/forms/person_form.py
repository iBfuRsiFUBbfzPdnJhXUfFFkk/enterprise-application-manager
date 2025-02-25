from django.forms import ModelForm

from core.models.person import Person


class PersonForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Person
