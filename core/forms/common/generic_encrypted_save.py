from django.db.models import Model
from django.forms import ModelForm


def generic_encrypted_save(
        model_form: ModelForm,
        instance: Model,
        data_points: list[str] | None = None,
) -> Model:
    if data_points is None:
        return instance
    for data_point in data_points:
        encrypted_value: str | None = model_form.cleaned_data[data_point]
        getattr(instance, f"set_{data_point}")(encrypted_value)
    instance.save()
    return instance
