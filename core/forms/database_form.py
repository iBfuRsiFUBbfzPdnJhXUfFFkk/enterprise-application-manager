from django.db.models import Model

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_encrypted_save import generic_encrypted_save
from core.models.database import Database


class DatabaseForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Database

    def save(self, commit: bool = True) -> Model:
        instance: Database = super().save(commit=False)
        return generic_encrypted_save(
            model_form=self,
            instance=instance,
            data_points=[
                "encrypted_password",
                "encrypted_username",
                "encrypted_ssh_tunnel_username",
                "encrypted_ssh_tunnel_password",
            ],
        )
