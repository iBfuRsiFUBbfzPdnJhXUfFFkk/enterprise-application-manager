from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Optional

from django.db.models import Q, QuerySet
from django.urls import reverse
from django.utils import timezone

from core.models.it_devops_request import ITDevOpsRequest
from core.models.maintenance_window import MaintenanceWindow
from core.models.release_bundle import ReleaseBundle
from core.models.sprint import Sprint

# Color scheme for event types (Tailwind CSS color names)
EVENT_COLORS = {
    'maintenance': '#EF4444',  # red-500
    'release': '#8B5CF6',      # violet-500
    'sprint': '#10B981',       # emerald-500
    'request': '#F59E0B',      # amber-500
}


@dataclass
class CalendarEvent:
    """Represents a unified calendar event from any source."""
    id: str  # Format: "type_id" e.g., "maintenance_123"
    title: str
    start: str  # ISO format datetime
    end: Optional[str]  # ISO format datetime
    all_day: bool
    color: str  # CSS color for event type
    event_type: str  # maintenance, release, sprint, request
    detail_url: str
    description: Optional[str] = None

    def to_dict(self):
        return asdict(self)


def get_calendar_events(start_date: date, end_date: date, event_types: list[str] | None = None) -> list[CalendarEvent]:
    """
    Aggregate calendar events from all sources within date range.

    Args:
        start_date: Start of date range
        end_date: End of date range
        event_types: List of event types to include (None = all)

    Returns:
        List of CalendarEvent objects sorted by start date
    """
    events = []

    if not event_types or 'maintenance' in event_types:
        events.extend(_get_maintenance_events(start_date, end_date))

    if not event_types or 'release' in event_types:
        events.extend(_get_release_events(start_date, end_date))

    if not event_types or 'sprint' in event_types:
        events.extend(_get_sprint_events(start_date, end_date))

    if not event_types or 'request' in event_types:
        events.extend(_get_request_events(start_date, end_date))

    # Sort by start date
    events.sort(key=lambda e: e.start)

    return events


def _get_maintenance_events(start_date: date, end_date: date) -> list[CalendarEvent]:
    """Get maintenance window events."""
    maintenance_windows: QuerySet[MaintenanceWindow] = MaintenanceWindow.objects.filter(
        Q(date_time_start__gte=start_date, date_time_start__lte=end_date) |
        Q(date_time_end__gte=start_date, date_time_end__lte=end_date) |
        Q(date_time_start__lte=start_date, date_time_end__gte=end_date)
    ).select_related('person_contact', 'person_created_by').prefetch_related('applications_affected')

    events = []
    for mw in maintenance_windows:
        start_dt = mw.date_time_start if mw.date_time_start else timezone.now()
        end_dt = mw.date_time_end if mw.date_time_end else start_dt

        events.append(CalendarEvent(
            id=f"maintenance_{mw.id}",
            title=mw.name if mw.name else 'Maintenance Window',
            start=start_dt.isoformat(),
            end=end_dt.isoformat(),
            all_day=False,
            color=EVENT_COLORS['maintenance'],
            event_type='maintenance',
            detail_url=reverse('maintenance_window_detail', kwargs={'model_id': mw.id}),
            description=mw.description if mw.description else None,
        ))

    return events


def _get_release_events(start_date: date, end_date: date) -> list[CalendarEvent]:
    """Get release bundle events (code freeze, demo, release dates)."""
    release_bundles: QuerySet[ReleaseBundle] = ReleaseBundle.objects.filter(
        Q(date_code_freeze__gte=start_date, date_code_freeze__lte=end_date) |
        Q(date_demo__gte=start_date, date_demo__lte=end_date) |
        Q(date_release__gte=start_date, date_release__lte=end_date)
    )

    events = []
    for rb in release_bundles:
        # Code freeze event
        if rb.date_code_freeze and start_date <= rb.date_code_freeze <= end_date:
            events.append(CalendarEvent(
                id=f"release_{rb.id}_freeze",
                title=f"{rb.name} - Code Freeze",
                start=datetime.combine(rb.date_code_freeze, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['release'],
                event_type='release',
                detail_url=reverse('release_bundle_detail', kwargs={'model_id': rb.id}),
                description=f"Code freeze for {rb.name}",
            ))

        # Demo event
        if rb.date_demo and start_date <= rb.date_demo <= end_date:
            events.append(CalendarEvent(
                id=f"release_{rb.id}_demo",
                title=f"{rb.name} - Demo",
                start=datetime.combine(rb.date_demo, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['release'],
                event_type='release',
                detail_url=reverse('release_bundle_detail', kwargs={'model_id': rb.id}),
                description=f"Demo for {rb.name}",
            ))

        # Release event
        if rb.date_release and start_date <= rb.date_release <= end_date:
            events.append(CalendarEvent(
                id=f"release_{rb.id}_release",
                title=f"{rb.name} - Release",
                start=datetime.combine(rb.date_release, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['release'],
                event_type='release',
                detail_url=reverse('release_bundle_detail', kwargs={'model_id': rb.id}),
                description=f"Release date for {rb.name}",
            ))

    return events


def _get_sprint_events(start_date: date, end_date: date) -> list[CalendarEvent]:
    """Get sprint schedule events."""
    sprints: QuerySet[Sprint] = Sprint.objects.filter(
        Q(date_start__gte=start_date, date_start__lte=end_date) |
        Q(date_end__gte=start_date, date_end__lte=end_date) |
        Q(date_start__lte=start_date, date_end__gte=end_date)
    )

    events = []
    for sprint in sprints:
        if sprint.date_start and sprint.date_end:
            events.append(CalendarEvent(
                id=f"sprint_{sprint.id}",
                title=sprint.name if sprint.name else 'Sprint',
                start=datetime.combine(sprint.date_start, datetime.min.time()).isoformat(),
                end=datetime.combine(sprint.date_end, datetime.max.time()).isoformat(),
                all_day=True,
                color=EVENT_COLORS['sprint'],
                event_type='sprint',
                detail_url=reverse('sprint_detail', kwargs={'model_id': sprint.id}),
                description=f"Sprint: {sprint.date_range_string}",
            ))

    return events


def _get_request_events(start_date: date, end_date: date) -> list[CalendarEvent]:
    """Get IT/DevOps request deadline events."""
    requests: QuerySet[ITDevOpsRequest] = ITDevOpsRequest.objects.filter(
        Q(date_requested__gte=start_date, date_requested__lte=end_date) |
        Q(date_due__gte=start_date, date_due__lte=end_date) |
        Q(date_completed__gte=start_date, date_completed__lte=end_date)
    ).select_related('person_requester', 'person_assignee', 'application')

    events = []
    for req in requests:
        # Requested date event
        if req.date_requested and start_date <= req.date_requested <= end_date:
            events.append(CalendarEvent(
                id=f"request_{req.id}_requested",
                title=f"{req.document_id or req.name} - Requested",
                start=datetime.combine(req.date_requested, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['request'],
                event_type='request',
                detail_url=reverse('it_devops_request_detail', kwargs={'model_id': req.id}),
                description=f"Request created: {req.name}",
            ))

        # Due date event
        if req.date_due and start_date <= req.date_due <= end_date:
            events.append(CalendarEvent(
                id=f"request_{req.id}_due",
                title=f"{req.document_id or req.name} - Due",
                start=datetime.combine(req.date_due, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['request'],
                event_type='request',
                detail_url=reverse('it_devops_request_detail', kwargs={'model_id': req.id}),
                description=f"Request due: {req.name}",
            ))

        # Completed date event
        if req.date_completed and start_date <= req.date_completed <= end_date:
            events.append(CalendarEvent(
                id=f"request_{req.id}_completed",
                title=f"{req.document_id or req.name} - Completed",
                start=datetime.combine(req.date_completed, datetime.min.time()).isoformat(),
                end=None,
                all_day=True,
                color=EVENT_COLORS['request'],
                event_type='request',
                detail_url=reverse('it_devops_request_detail', kwargs={'model_id': req.id}),
                description=f"Request completed: {req.name}",
            ))

    return events
