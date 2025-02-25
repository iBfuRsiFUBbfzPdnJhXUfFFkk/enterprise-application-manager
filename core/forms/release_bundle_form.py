from django.forms import ModelForm

from core.forms.common.generic_date_field import generic_date_field
from core.models.release_bundle import ReleaseBundle


class ReleaseBundleForm(ModelForm):
    date_code_freeze = generic_date_field()
    date_demo = generic_date_field()
    date_release = generic_date_field()

    class Meta:
        fields = '__all__'
        model = ReleaseBundle
