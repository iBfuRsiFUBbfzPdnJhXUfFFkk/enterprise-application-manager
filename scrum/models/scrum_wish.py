from django.db import models

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.models.person import Person
from core.models.project import Project


class ScrumWish(
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractStartEndDates,
):
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    application_group = models.ForeignKey(ApplicationGroup, on_delete=models.SET_NULL, null=True, blank=True)
    person_submitted_by = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Scrum Wish"
        verbose_name_plural = "Scrum Wishes"
