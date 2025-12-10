from django.forms import DateInput

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.recommendation import Recommendation


class RecommendationForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Recommendation
        widgets = {
            "date_recommended": DateInput(attrs={"type": "date"}),
            "date_target_completion": DateInput(attrs={"type": "date"}),
            "date_completed": DateInput(attrs={"type": "date"}),
        }
