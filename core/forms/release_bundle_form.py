from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_date_field import generic_date_field
from core.models.release_bundle import ReleaseBundle


class ReleaseBundleForm(BaseModelForm):
    date_code_freeze = generic_date_field()
    date_demo = generic_date_field()
    date_release = generic_date_field()

    class Meta(BaseModelFormMeta):
        model = ReleaseBundle
