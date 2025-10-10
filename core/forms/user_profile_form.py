from django import forms
from core.models.user import User


class UserProfileForm(forms.ModelForm):
    """
    Form for users to update their own profile information.
    """

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'employee_company',
            'employee_department',
            'employee_number',
            'employee_telephone',
            'employee_title',
            'comment',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'employee_company': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_department': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_title': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
