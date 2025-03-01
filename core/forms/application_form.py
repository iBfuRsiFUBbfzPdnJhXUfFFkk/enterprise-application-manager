from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_choice_field import generic_choice_field
from core.forms.common.generic_date_field import generic_date_field
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.forms.common.generic_person_choice_field import generic_person_choice_field
from core.forms.common.generic_person_multiple_choice_field import generic_person_multiple_choice_field
from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool


class ApplicationForm(BaseModelForm):
    application_group_platform = generic_choice_field(queryset=ApplicationGroup.objects.filter(is_platform=True))
    application_groups = generic_multiple_choice_field(queryset=ApplicationGroup.objects.all())
    date_launch = generic_date_field()
    person_architect = generic_person_choice_field(is_architect=True)
    person_developers = generic_person_multiple_choice_field(is_developer=True)
    person_lead_developer = generic_person_choice_field(is_lead_developer=True)
    person_product_manager = generic_person_choice_field(is_product_manager=True)
    person_product_owner = generic_person_choice_field(is_product_owner=True)
    person_project_manager = generic_person_choice_field(is_project_manager=True)
    person_scrum_master = generic_person_choice_field(is_scrum_master=True)
    person_stakeholders = generic_person_multiple_choice_field(is_stakeholder=True)
    service_providers = generic_multiple_choice_field(queryset=ServiceProvider.objects.all())
    tools = generic_multiple_choice_field(queryset=Tool.objects.all())

    class Meta(BaseModelFormMeta):
        model = Application
