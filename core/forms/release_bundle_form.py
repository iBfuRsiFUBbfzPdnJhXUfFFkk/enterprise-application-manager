from django.forms import ModelForm, DateInput, DateField

from core.models.release_bundle import ReleaseBundle


class ReleaseBundleForm(ModelForm):
    date_code_freeze = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )
    date_demo = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )
    date_release = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        fields = '__all__'
        model = ReleaseBundle
