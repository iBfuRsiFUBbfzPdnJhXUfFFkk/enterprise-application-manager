from django.urls import URLPattern, URLResolver, path

from core.views.calendar.calendar_events_api_view import calendar_events_api_view
from core.views.calendar.calendar_view import calendar_view

urlpatterns_calendar: list[URLPattern | URLResolver] = [
    path(name='calendar', route='calendar/', view=calendar_view),
    path(name='calendar_events_api', route='calendar/api/events/', view=calendar_events_api_view),
]
