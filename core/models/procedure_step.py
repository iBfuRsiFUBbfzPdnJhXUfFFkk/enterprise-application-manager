from django.core.exceptions import ValidationError
from django.db import models

from core.models.command import CommandLanguage
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class ProcedureStepType:
    """Step type choices for procedure steps"""
    MARKDOWN = 'markdown'
    CODE = 'code'
    FILE_REFERENCE = 'file_reference'
    CHECKLIST = 'checklist'

    CHOICES = [
        (MARKDOWN, 'Markdown Text'),
        (CODE, 'Code Block'),
        (FILE_REFERENCE, 'File Reference'),
        (CHECKLIST, 'Checklist Item'),
    ]


class ProcedureStep(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Ordered procedural step for an Application.
    Each application can have multiple steps forming a complete procedure.
    Supports markdown, code blocks, file references, and checklists.
    """

    application = models.ForeignKey(
        'Application',
        on_delete=models.CASCADE,
        related_name='procedure_steps',
        help_text='Application this step belongs to'
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order of this step (lower numbers appear first)'
    )

    step_type = models.CharField(
        max_length=50,
        choices=ProcedureStepType.CHOICES,
        default=ProcedureStepType.MARKDOWN,
        help_text='Type of procedure step'
    )

    step_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Type-specific configuration stored as JSON'
    )

    class Meta:
        ordering = ['application', 'order', 'id']
        indexes = [
            models.Index(fields=['application', 'order']),
        ]

    def __str__(self):
        app_name = self.application.acronym or self.application.name if self.application else 'Unknown'
        return f"{app_name} - Step {self.order}: {self.name}"

    def clean(self):
        """Validate step_data based on step_type"""
        super().clean()

        if not isinstance(self.step_data, dict):
            raise ValidationError({'step_data': 'Step data must be a dictionary'})

        if self.step_type == ProcedureStepType.MARKDOWN:
            if 'content' not in self.step_data:
                raise ValidationError({'step_data': 'Markdown steps must have "content" field'})

        elif self.step_type == ProcedureStepType.CODE:
            if 'code' not in self.step_data:
                raise ValidationError({'step_data': 'Code steps must have "code" field'})
            if 'language' not in self.step_data:
                raise ValidationError({'step_data': 'Code steps must have "language" field'})
            # Validate language is valid
            valid_languages = [choice[0] for choice in CommandLanguage.CHOICES]
            if self.step_data.get('language') not in valid_languages:
                raise ValidationError({'step_data': f'Invalid language. Must be one of: {", ".join(valid_languages)}'})

        elif self.step_type == ProcedureStepType.FILE_REFERENCE:
            if 'file_path' not in self.step_data:
                raise ValidationError({'step_data': 'File reference steps must have "file_path" field'})

        elif self.step_type == ProcedureStepType.CHECKLIST:
            if 'items' not in self.step_data:
                raise ValidationError({'step_data': 'Checklist steps must have "items" field'})
            if not isinstance(self.step_data.get('items'), list):
                raise ValidationError({'step_data': 'Checklist items must be a list'})
            # Validate each item has required fields
            for i, item in enumerate(self.step_data.get('items', [])):
                if not isinstance(item, dict):
                    raise ValidationError({'step_data': f'Checklist item {i} must be a dictionary'})
                if 'text' not in item:
                    raise ValidationError({'step_data': f'Checklist item {i} must have "text" field'})

    def get_rendered_content(self):
        """Returns content preview based on step type"""
        if self.step_type == ProcedureStepType.MARKDOWN:
            return self.step_data.get('content', '')[:100]
        elif self.step_type == ProcedureStepType.CODE:
            return f"{self.step_data.get('language', 'code')}: {self.step_data.get('code', '')[:100]}"
        elif self.step_type == ProcedureStepType.FILE_REFERENCE:
            return self.step_data.get('file_path', '')
        elif self.step_type == ProcedureStepType.CHECKLIST:
            items = self.step_data.get('items', [])
            return f"{len(items)} checklist items"
        return ''
