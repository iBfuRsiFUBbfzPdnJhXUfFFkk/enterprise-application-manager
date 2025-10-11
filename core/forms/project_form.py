from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.project import Project


class ProjectForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Project
