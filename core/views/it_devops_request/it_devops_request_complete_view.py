from datetime import date, datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.common.enums.it_devops_request_status_choices import IT_DEVOPS_REQUEST_STATUS_COMPLETED
from core.models.it_devops_request import ITDevOpsRequest


def it_devops_request_complete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Mark an IT/DevOps request as complete."""
    if request.method != "POST":
        return redirect('it_devops_request_detail', model_id=model_id)

    it_devops_request: ITDevOpsRequest = get_object_or_404(ITDevOpsRequest, id=model_id)

    client_date = parse_client_date(request.POST.get('date_completed', ''))
    it_devops_request.status = IT_DEVOPS_REQUEST_STATUS_COMPLETED
    it_devops_request.date_completed = client_date
    it_devops_request.save()

    messages.success(request, f"Request '{it_devops_request.name}' marked as complete!")
    return redirect('it_devops_request_detail', model_id=model_id)


def parse_client_date(raw_date: str) -> date:
    """Parse a YYYY-MM-DD string into a date, falling back to today."""
    try:
        return datetime.strptime(raw_date.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return date.today()
