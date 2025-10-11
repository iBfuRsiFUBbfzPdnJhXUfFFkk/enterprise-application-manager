from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.software_bill_of_material import SoftwareBillOfMaterial


class SoftwareBillOfMaterialForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = SoftwareBillOfMaterial
