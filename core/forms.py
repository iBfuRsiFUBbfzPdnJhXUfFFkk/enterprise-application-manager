from django.forms import ModelForm

from core.models import Application, Person


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'