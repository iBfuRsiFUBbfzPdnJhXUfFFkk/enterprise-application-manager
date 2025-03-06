from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


class KeyPerformanceIndicatorSprint(BaseModel, Comment):
    cached_capacity_adjusted = create_generic_integer()
    cached_capacity_per_day = create_generic_decimal()
    capacity_base = create_generic_integer()
    number_of_code_lines_added = create_generic_integer()
    number_of_code_lines_removed = create_generic_integer()
    number_of_comments_made = create_generic_integer()
    number_of_context_switches = create_generic_integer()
    number_of_issues_written = create_generic_integer()
    number_of_merge_requests_approved = create_generic_integer()
    number_of_paid_time_off_days = create_generic_integer()
    number_of_story_points_committed_to = create_generic_integer()
    number_of_story_points_delivered = create_generic_integer()
    number_of_threads_made = create_generic_integer()
    person_developer = create_generic_fk(to=Person)
    sprint = create_generic_fk(to=Sprint)

    @property
    def coerced_base_capacity(self) -> int:
        if self.capacity_base is not None:
            return self.capacity_base
        person: Person | None = self.person_developer
        if person is not None:
            return person.coerced_base_capacity
        current_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
        return current_server_configuration.coerced_base_capacity

    def __str__(self):
        return f"{str(self.id)} | {str(self.person_developer)} | {str(self.sprint)}"

    class Meta:
        ordering = ['-id']
