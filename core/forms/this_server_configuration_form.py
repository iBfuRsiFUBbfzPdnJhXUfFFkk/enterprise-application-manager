from django.forms import SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_choice_field import generic_choice_field
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.person import Person
from core.models.role import Role
from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration


class ThisServerConfigurationForm(BaseModelForm):
    connection_git_lab_token = generic_choice_field(queryset=Secret.objects.all())
    connection_google_maps_api_key = generic_choice_field(queryset=Secret.objects.all())
    connection_chatgpt_api_key = generic_choice_field(queryset=Secret.objects.all())
    kpi_developers_to_exclude = generic_multiple_choice_field(queryset=Person.objects.all())
    type_developer_role = generic_choice_field(queryset=Role.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update multi-select field to use SelectMultiple widget with Select2
        if 'kpi_developers_to_exclude' in self.fields:
            field = self.fields['kpi_developers_to_exclude']
            field.widget = SelectMultiple(attrs={'class': 'select2-kpi-developers-to-exclude'})
            field.widget.choices = field.choices

    class Meta(BaseModelFormMeta):
        model = ThisServerConfiguration
