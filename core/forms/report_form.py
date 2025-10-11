from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.report import Report


class ReportForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Report
