from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_text import create_generic_text

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class Recommendation(AbstractBaseModel, AbstractComment, AbstractName):
    # Optional relationships
    application = create_generic_fk(to="Application", related_name="recommendations")
    project = create_generic_fk(to="Project", related_name="recommendations")
    estimation = create_generic_fk(to="Estimation", related_name="recommendations")
    person_recommended_by = create_generic_fk(to="Person", related_name="recommendations_made")
    links = create_generic_m2m(to="Link", related_name="recommendations")

    # Core content fields (TextField for multi-line markdown content)
    description = create_generic_text()
    rationale = create_generic_text()
    benefits = create_generic_text()
    risks = create_generic_text()

    # Date tracking
    date_recommended = create_generic_date()

    def __str__(self):
        return self.name or "Untitled Recommendation"

    class Meta:
        ordering = ["-date_recommended", "-id"]
