from django_generic_model_fields.create_generic_fk import create_generic_fk

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
    application = create_generic_fk(to=Application)
    application_group = create_generic_fk(to=ApplicationGroup)
    person_submitted_by = create_generic_fk(to=Person)
    project = create_generic_fk(to=Project)

    class Meta:
        ordering = ['-id']
        verbose_name = "Scrum Wish"
        verbose_name_plural = "Scrum Wishes"
