from datetime import date, datetime, timedelta

from django.http import HttpRequest, JsonResponse

from core.utilities.calendar.calendar_event_aggregator import get_calendar_events


def calendar_events_api_view(request: HttpRequest) -> JsonResponse:
    """
    API endpoint for fetching calendar events.

    Query params:
        - start: ISO date string (YYYY-MM-DD)
        - end: ISO date string (YYYY-MM-DD)
        - types: Comma-separated event types
    """
    # Parse query params
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    types_str = request.GET.get('types', '')

    # Validate and parse dates
    try:
        start_date = datetime.fromisoformat(start_str).date() if start_str else date.today()
        end_date = datetime.fromisoformat(end_str).date() if end_str else start_date + timedelta(days=30)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Parse event types
    event_types = [t.strip() for t in types_str.split(',') if t.strip()] if types_str else None

    # Get events
    events = get_calendar_events(start_date, end_date, event_types)

    # Return JSON
    return JsonResponse({
        'events': [event.to_dict() for event in events],
        'start': start_date.isoformat(),
        'end': end_date.isoformat(),
    })
