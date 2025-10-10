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
    kpi_developers_to_exclude = generic_multiple_choice_field(queryset=Person.objects.all())
    type_developer_role = generic_choice_field(queryset=Role.objects.all())

    class Meta(BaseModelFormMeta):
        model = ThisServerConfiguration
