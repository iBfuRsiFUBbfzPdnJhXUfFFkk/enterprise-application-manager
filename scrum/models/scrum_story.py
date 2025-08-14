from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates


class ScrumStory(
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractStartEndDates,
):

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-date_end', '-id']
        verbose_name = "Scrum Story"
        verbose_name_plural = "Scrum Stories"
