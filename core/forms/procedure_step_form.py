import json

from django import forms
from django.core.exceptions import ValidationError

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.command import CommandLanguage
from core.models.procedure_step import ProcedureStep, ProcedureStepType


class ProcedureStepForm(BaseModelForm):
    """
    Form for creating and editing procedure steps.
    Handles dynamic fields based on step_type.
    """

    # Type-specific fields for markdown
    markdown_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter markdown content...'
        }),
        required=False,
        label='Markdown Content'
    )

    # Type-specific fields for code
    code_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono',
            'placeholder': 'Enter code...'
        }),
        required=False,
        label='Code'
    )
    code_language = forms.ChoiceField(
        choices=CommandLanguage.CHOICES,
        initial=CommandLanguage.BASH,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        required=False,
        label='Programming Language'
    )

    # Type-specific fields for file reference
    file_path = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono',
            'placeholder': '/path/to/file'
        }),
        required=False,
        label='File Path'
    )
    file_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Description of the file...'
        }),
        required=False,
        label='Description'
    )

    # Type-specific fields for checklist
    checklist_items = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'One item per line'
        }),
        required=False,
        label='Checklist Items',
        help_text='Enter one item per line'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize step_type field
        self.fields['step_type'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'id': 'id_step_type'
        })

        # Customize name field
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Step name...'
        })

        # Customize comment field
        self.fields['comment'].widget.attrs.update({
            'rows': 3,
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Additional notes (optional)...'
        })
        self.fields['comment'].required = False

        # Hide application and order fields
        self.fields['application'].widget = forms.HiddenInput()
        self.fields['order'].widget = forms.HiddenInput()

        # Hide step_data field (we'll build it from type-specific fields)
        self.fields['step_data'].widget = forms.HiddenInput()
        self.fields['step_data'].required = False

        # Pre-populate type-specific fields if editing existing step
        if self.instance and self.instance.pk:
            step_data = self.instance.step_data or {}
            step_type = self.instance.step_type

            if step_type == ProcedureStepType.MARKDOWN:
                self.fields['markdown_content'].initial = step_data.get('content', '')

            elif step_type == ProcedureStepType.CODE:
                self.fields['code_content'].initial = step_data.get('code', '')
                self.fields['code_language'].initial = step_data.get('language', CommandLanguage.BASH)

            elif step_type == ProcedureStepType.FILE_REFERENCE:
                self.fields['file_path'].initial = step_data.get('file_path', '')
                self.fields['file_description'].initial = step_data.get('description', '')

            elif step_type == ProcedureStepType.CHECKLIST:
                items = step_data.get('items', [])
                items_text = '\n'.join([item.get('text', '') for item in items])
                self.fields['checklist_items'].initial = items_text

    def clean(self):
        cleaned_data = super().clean()
        step_type = cleaned_data.get('step_type')

        # Build step_data based on step_type
        step_data = {}

        if step_type == ProcedureStepType.MARKDOWN:
            content = cleaned_data.get('markdown_content', '').strip()
            if not content:
                raise ValidationError({'markdown_content': 'Markdown content is required for markdown steps'})
            step_data = {'content': content}

        elif step_type == ProcedureStepType.CODE:
            code = cleaned_data.get('code_content', '').strip()
            language = cleaned_data.get('code_language')
            if not code:
                raise ValidationError({'code_content': 'Code is required for code steps'})
            step_data = {'code': code, 'language': language}

        elif step_type == ProcedureStepType.FILE_REFERENCE:
            file_path = cleaned_data.get('file_path', '').strip()
            description = cleaned_data.get('file_description', '').strip()
            if not file_path:
                raise ValidationError({'file_path': 'File path is required for file reference steps'})
            step_data = {'file_path': file_path, 'description': description}

        elif step_type == ProcedureStepType.CHECKLIST:
            items_text = cleaned_data.get('checklist_items', '').strip()
            if not items_text:
                raise ValidationError({'checklist_items': 'At least one checklist item is required'})
            items = [{'text': line.strip(), 'completed': False} for line in items_text.split('\n') if line.strip()]
            if not items:
                raise ValidationError({'checklist_items': 'At least one checklist item is required'})
            step_data = {'items': items}

        cleaned_data['step_data'] = step_data
        return cleaned_data

    class Meta(BaseModelFormMeta):
        model = ProcedureStep
        fields = ['name', 'step_type', 'application', 'order', 'comment', 'step_data']
