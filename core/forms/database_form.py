from django.forms import ModelForm

from core.models.database import Database


class DatabaseForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Database
