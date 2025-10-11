from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.task import Task


class TaskForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Task
