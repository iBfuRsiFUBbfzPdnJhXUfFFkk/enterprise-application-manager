from django.forms import DateField, DateInput


def generic_date_field() -> DateField:
    return DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date'}),
    )
