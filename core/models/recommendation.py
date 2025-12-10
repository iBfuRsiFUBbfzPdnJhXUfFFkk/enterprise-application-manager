from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


# Priority choices
RECOMMENDATION_PRIORITY_HIGH = "High"
RECOMMENDATION_PRIORITY_MEDIUM = "Medium"
RECOMMENDATION_PRIORITY_LOW = "Low"

RECOMMENDATION_PRIORITY_CHOICES = [
    (RECOMMENDATION_PRIORITY_HIGH, RECOMMENDATION_PRIORITY_HIGH),
    (RECOMMENDATION_PRIORITY_MEDIUM, RECOMMENDATION_PRIORITY_MEDIUM),
    (RECOMMENDATION_PRIORITY_LOW, RECOMMENDATION_PRIORITY_LOW),
]

# Status choices
RECOMMENDATION_STATUS_PROPOSED = "Proposed"
RECOMMENDATION_STATUS_UNDER_REVIEW = "Under Review"
RECOMMENDATION_STATUS_APPROVED = "Approved"
RECOMMENDATION_STATUS_REJECTED = "Rejected"
RECOMMENDATION_STATUS_IMPLEMENTED = "Implemented"

RECOMMENDATION_STATUS_CHOICES = [
    (RECOMMENDATION_STATUS_PROPOSED, RECOMMENDATION_STATUS_PROPOSED),
    (RECOMMENDATION_STATUS_UNDER_REVIEW, RECOMMENDATION_STATUS_UNDER_REVIEW),
    (RECOMMENDATION_STATUS_APPROVED, RECOMMENDATION_STATUS_APPROVED),
    (RECOMMENDATION_STATUS_REJECTED, RECOMMENDATION_STATUS_REJECTED),
    (RECOMMENDATION_STATUS_IMPLEMENTED, RECOMMENDATION_STATUS_IMPLEMENTED),
]


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

    # Classification
    priority = create_generic_enum(choices=RECOMMENDATION_PRIORITY_CHOICES)
    status = create_generic_enum(choices=RECOMMENDATION_STATUS_CHOICES)

    # Date tracking
    date_recommended = create_generic_date()
    date_target_completion = create_generic_date()
    date_completed = create_generic_date()

    def __str__(self):
        return f"{self.name} - {self.priority} ({self.status})"

    class Meta:
        ordering = ["-date_recommended", "priority", "-id"]
