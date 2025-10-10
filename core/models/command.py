from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class CommandLanguage:
    BASH = 'bash'
    PYTHON = 'python'
    JAVASCRIPT = 'javascript'
    SQL = 'sql'
    OTHER = 'other'

    CHOICES = [
        (BASH, 'Bash'),
        (PYTHON, 'Python'),
        (JAVASCRIPT, 'JavaScript'),
        (SQL, 'SQL'),
        (OTHER, 'Other'),
    ]


class Command(AbstractBaseModel, AbstractComment, AbstractName):
    command = create_generic_varchar()
    language = create_generic_enum(choices=CommandLanguage.CHOICES)

    def __str__(self):
        return f"{self.name} {self.command}"

    def is_python(self):
        return self.language == CommandLanguage.PYTHON

    def save(self, *args, **kwargs):
        # Set default language to bash if not specified
        if not self.language:
            self.language = CommandLanguage.BASH
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name', '-id']
