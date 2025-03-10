from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.utilities.cast_query_set import cast_query_set


class ScrumSprint(
    AbstractAlias,
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractStartEndDates,
):
    @property
    def iterations(self):
        from git_lab.models.git_lab_iteration import GitLabIteration
        return cast_query_set(
            typ=GitLabIteration,
            val=GitLabIteration.objects.filter(group=self)
        )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-date_end', '-id']
        verbose_name = "Scrum Sprint"
        verbose_name_plural = "Scrum Sprints"
