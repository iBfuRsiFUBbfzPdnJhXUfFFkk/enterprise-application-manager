from django.forms import ModelForm, DateInput

from core.models import Application, Person


class ApplicationForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Application
        widgets = {'date_launch': DateInput(attrs={'type': 'date'})}

class PersonForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Person