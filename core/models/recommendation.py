
from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName

class Recommendation(AbstractBaseModel, AbstractComment, AbstractName):
    # Optional relationships
    application = models.ForeignKey("Application", on_delete=models.SET_NULL, null=True, blank=True, related_name="recommendations")
    project = models.ForeignKey("Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="recommendations")
    estimation = models.ForeignKey("Estimation", on_delete=models.SET_NULL, null=True, blank=True, related_name="recommendations")
    person_recommended_by = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="recommendations_made")
    links = models.ManyToManyField("Link", blank=True, related_name="recommendations")

    # Core content fields (TextField for multi-line markdown content)
    description = models.TextField(null=True, blank=True)
    rationale = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)

    # Date tracking
    date_recommended = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name or "Untitled Recommendation"

    class Meta:
        ordering = ["-date_recommended", "-id"]
