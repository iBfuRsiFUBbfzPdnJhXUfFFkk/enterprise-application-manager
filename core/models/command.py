from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


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
    command = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, choices=CommandLanguage.CHOICES, null=True, blank=True)

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
