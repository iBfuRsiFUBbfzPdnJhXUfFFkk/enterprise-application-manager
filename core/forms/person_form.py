from django.forms import ModelForm

from core.forms.common.generic_date_field import generic_date_field
from core.models.person import Person


class PersonForm(ModelForm):
    date_birthday = generic_date_field()
    date_hired = generic_date_field()
    date_left = generic_date_field()

    class Meta:
        fields = '__all__'
        model = Person
