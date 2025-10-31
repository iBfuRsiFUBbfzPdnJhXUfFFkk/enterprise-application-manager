from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.billing_code import BillingCode
from core.models.project import Project


class BillingCodeForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = BillingCode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize projects field display
        if 'projects' in self.fields:
            self.fields['projects'].queryset = Project.objects.all().order_by('name')
            self.fields['projects'].label_from_instance = lambda obj: obj.name
