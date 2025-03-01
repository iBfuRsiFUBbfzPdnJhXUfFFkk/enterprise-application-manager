from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.application import Application
from core.models.dependency import Dependency


class DependencyForm(BaseModelForm):
    applications = generic_multiple_choice_field(queryset=Application.objects.all())

    class Meta(BaseModelFormMeta):
        model = Dependency
