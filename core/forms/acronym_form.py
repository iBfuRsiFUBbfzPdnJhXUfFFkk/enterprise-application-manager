from django.forms import ModelForm, Textarea

from core.models.acronym import Acronym
from core.models.common.extensions.string_list_field import StringListField


class AcronymForm(ModelForm):
    supporting_links = StringListField(widget=Textarea)

    class Meta:
        fields = '__all__'
        model = Acronym
