from django.db.models import QuerySet

from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from core.utilities.get_name_acronym import get_name_acronym


class JobTitle(
    AbstractAcronym,
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
):
    @property
    def people_with_this_job_title(self) -> QuerySet:
        from core.models.person import Person
        return cast_query_set(
            typ=Person,
            val=Person.objects.filter(job_title=self)
        )

    def __str__(self) -> str:
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"
