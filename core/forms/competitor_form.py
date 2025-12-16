from django.forms import NumberInput

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.competitor import Competitor


class CompetitorForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Competitor
        widgets = {
            'year_founded': NumberInput(attrs={'min': '1800', 'max': '2100'}),
        }
