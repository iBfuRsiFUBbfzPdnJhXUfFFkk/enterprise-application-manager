from django.db.models import Model

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_encrypted_save import generic_encrypted_save
from core.models.secret import Secret


class SecretForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Secret

    def save(self, commit: bool = True) -> Model:
        instance: Secret = super().save(commit=False)
        return generic_encrypted_save(
            model_form=self,
            instance=instance,
            data_points=["encrypted_value"],
        )
