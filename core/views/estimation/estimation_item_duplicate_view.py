from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_item_duplicate_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Duplicate an estimation item with all its values."""
    try:
        original_item = EstimationItem.objects.get(id=item_id)
        estimation_id = original_item.estimation.id

        # Create a new item with all the same values
        # We don't set pk, so Django will create a new record
        # Append " (Copy)" to title if it exists
        new_title = f"{original_item.title} (Copy)" if original_item.title else None

        new_item = EstimationItem(
            estimation=original_item.estimation,
            title=new_title,
            description=original_item.description,
            story_points=original_item.story_points,
            hours_junior=original_item.hours_junior,
            hours_mid=original_item.hours_mid,
            hours_senior=original_item.hours_senior,
            hours_lead=original_item.hours_lead,
            code_review_hours_junior=original_item.code_review_hours_junior,
            code_review_hours_mid=original_item.code_review_hours_mid,
            code_review_hours_senior=original_item.code_review_hours_senior,
            code_review_hours_lead=original_item.code_review_hours_lead,
            code_reviewer_hours=original_item.code_reviewer_hours,
            tests_hours_junior=original_item.tests_hours_junior,
            tests_hours_mid=original_item.tests_hours_mid,
            tests_hours_senior=original_item.tests_hours_senior,
            tests_hours_lead=original_item.tests_hours_lead,
            cone_of_uncertainty=original_item.cone_of_uncertainty,
            complexity_level=original_item.complexity_level,
            priority=original_item.priority,
        )
        # The save() method will auto-assign the order
        new_item.save()

    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=estimation_id)
