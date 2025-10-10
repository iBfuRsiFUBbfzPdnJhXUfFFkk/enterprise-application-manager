from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.job_title import JobTitle


class JobTitleForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = JobTitle
