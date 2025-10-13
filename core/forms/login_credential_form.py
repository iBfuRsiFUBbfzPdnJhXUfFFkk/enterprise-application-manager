from django.db.models import Model

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_encrypted_save import generic_encrypted_save
from core.models.login_credential import LoginCredential


class LoginCredentialForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = LoginCredential

    def save(self, commit: bool = True) -> Model:
        instance: LoginCredential = super().save(commit=False)
        return generic_encrypted_save(
            model_form=self,
            instance=instance,
            data_points=["encrypted_password"],
        )
