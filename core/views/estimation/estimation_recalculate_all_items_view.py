from decimal import Decimal

from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation import Estimation
from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_recalculate_all_items_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Recalculate all hours and story points for all items in the estimation using auto-calculation logic.
    Uses lead dev hours as the base and applies reverse multipliers, then calculates
    code review (0.5x), testing (1x), code reviewer (1x of lead code review) hours, and story points.
    Story points calculated as: base_hours / 4 (1 story point ≈ 4 hours), rounded to nearest 0.5.
    """
    try:
        estimation = Estimation.objects.get(id=model_id)
        items = EstimationItem.objects.filter(estimation=estimation)

        # Reverse multipliers to calculate from lead to other levels
        # Since final hours = base * multiplier, to get equal final hours:
        # If lead does 10 hours (1x multiplier) = 10 final hours
        # Senior needs 12.5 hours (1.5x multiplier) = 18.75 final hours
        # Wait, that's not right. Let me think...

        # Actually, the user wants to auto-populate based on lead hours.
        # When lead dev = 10:
        # - Lead final = 10 * 1.0 = 10
        # - Senior should be adjusted so: senior * 1.5 ≈ lead * 1.0, so senior = lead / 1.5 * 1.0 = lead * 0.667
        # - Mid should be: mid * 3.0 ≈ lead * 1.0, so mid = lead / 3.0 * 1.0 = lead * 0.333
        # - Junior should be: junior * 6.0 ≈ lead * 1.0, so junior = lead / 6.0 * 1.0 = lead * 0.167

        # Wait, let me reconsider. Looking at the JavaScript in the form, it does:
        # senior = lead * 1.25
        # mid = lead * 2
        # junior = lead * 3

        # That means they want the base hours to scale up, not the final hours to match.
        # So senior base hours are higher than lead, which when multiplied by 1.5x gives even higher final.

        # Let me check the form again... Yes, the reverse multipliers are:
        # senior = lead * 1.25
        # mid = lead * 2
        # junior = lead * 3

        REVERSE_MULTIPLIERS = {
            'SENIOR': Decimal('1.25'),
            'MID': Decimal('2.0'),
            'JUNIOR': Decimal('3.0'),
        }

        with transaction.atomic():
            for item in items:
                # Use lead dev hours as the base
                lead_hours = item.hours_lead or Decimal('0')

                if lead_hours > 0:
                    # Calculate other level dev hours
                    item.hours_senior = lead_hours * REVERSE_MULTIPLIERS['SENIOR']
                    item.hours_mid = lead_hours * REVERSE_MULTIPLIERS['MID']
                    item.hours_junior = lead_hours * REVERSE_MULTIPLIERS['JUNIOR']

                    # Calculate code review hours (0.5x of dev hours)
                    item.code_review_hours_lead = lead_hours * Decimal('0.5')
                    item.code_review_hours_senior = item.hours_senior * Decimal('0.5')
                    item.code_review_hours_mid = item.hours_mid * Decimal('0.5')
                    item.code_review_hours_junior = item.hours_junior * Decimal('0.5')

                    # Calculate testing hours (1x of dev hours)
                    item.tests_hours_lead = lead_hours
                    item.tests_hours_senior = item.hours_senior
                    item.tests_hours_mid = item.hours_mid
                    item.tests_hours_junior = item.hours_junior

                    # Calculate code reviewer hours (1x of lead code review hours)
                    item.code_reviewer_hours = item.code_review_hours_lead

                    # Calculate story points based on lead dev base hours
                    item.story_points = item.calculate_story_points()

                # Save the item with updated fields
                item.save(update_fields=[
                    'hours_senior', 'hours_mid', 'hours_junior',
                    'code_review_hours_lead', 'code_review_hours_senior',
                    'code_review_hours_mid', 'code_review_hours_junior',
                    'tests_hours_lead', 'tests_hours_senior',
                    'tests_hours_mid', 'tests_hours_junior',
                    'code_reviewer_hours', 'story_points'
                ])

    except Estimation.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=model_id)
