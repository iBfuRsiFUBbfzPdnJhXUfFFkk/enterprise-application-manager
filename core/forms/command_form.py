from django import forms
from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.command import Command, CommandLanguage


class CommandForm(BaseModelForm):
    # Override the command field to use a textarea widget for better code input
    command = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 15,
            'class': 'font-mono text-sm',
            'placeholder': 'Enter your command or code here...'
        }),
        required=True,
        help_text='Enter the command or code snippet'
    )

    # Override language field for better display
    language = forms.ChoiceField(
        choices=CommandLanguage.CHOICES,
        initial=CommandLanguage.BASH,
        required=True,
        help_text='Select the programming language'
    )

    class Meta(BaseModelFormMeta):
        model = Command
        fields = ['name', 'language', 'command', 'comment']
