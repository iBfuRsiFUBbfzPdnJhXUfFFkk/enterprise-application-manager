from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class Recommendation(AbstractBaseModel, AbstractComment, AbstractName):
    # Optional relationships
    application = create_generic_fk(to="Application", related_name="recommendations")
    project = create_generic_fk(to="Project", related_name="recommendations")
    estimation = create_generic_fk(to="Estimation", related_name="recommendations")
    person_recommended_by = create_generic_fk(to="Person", related_name="recommendations_made")

    # Core content fields
    description = create_generic_varchar()
    rationale = create_generic_varchar()
    benefits = create_generic_varchar()
    risks = create_generic_varchar()

    # Date tracking
    date_recommended = create_generic_date()

    def __str__(self):
        return self.name or "Untitled Recommendation"

    class Meta:
        ordering = ["-date_recommended", "-id"]
