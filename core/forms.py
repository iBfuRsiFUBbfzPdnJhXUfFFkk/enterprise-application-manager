from django.forms import ModelForm, DateInput

from core.models.application import Application
from core.models.database import Database
from core.models.dependency import Dependency
from core.models.person import Person
from core.models.release import Release
from core.models.release_bundle import ReleaseBundle


class ApplicationForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Application
        widgets = {'date_launch': DateInput(attrs={'type': 'date'})}


class DatabaseForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Database


class DependencyForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Dependency


class PersonForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Person


class ReleaseForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Release


class ReleaseBundleForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = ReleaseBundle
