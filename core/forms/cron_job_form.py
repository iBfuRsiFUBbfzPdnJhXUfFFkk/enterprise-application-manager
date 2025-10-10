from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.cron_job import CronJob


class CronJobForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = CronJob
