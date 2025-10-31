from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.billing_code import BillingCode
from core.models.person import Person
from core.models.project import Project
from core.models.role import Role


class ProjectForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Project

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter project_manager field to only show people with the Project Manager role
        if 'project_manager' in self.fields:
            try:
                project_manager_role = Role.objects.get(name='Project Manager')
                self.fields['project_manager'].queryset = Person.objects.filter(
                    roles=project_manager_role
                ).order_by('name_last', 'name_first')
                self.fields['project_manager'].label_from_instance = lambda obj: f"{obj.name_last}, {obj.name_first}" if obj.name_last and obj.name_first else str(obj)
            except Role.DoesNotExist:
                # If the role doesn't exist, show all people but add a note
                self.fields['project_manager'].help_text = 'Warning: Project Manager role not found.'

        # Customize billing_codes field display
        if 'billing_codes' in self.fields:
            self.fields['billing_codes'].queryset = BillingCode.objects.all().order_by('billing_code', 'name')
            self.fields['billing_codes'].label_from_instance = lambda obj: f"{obj.billing_code} - {obj.name}"
