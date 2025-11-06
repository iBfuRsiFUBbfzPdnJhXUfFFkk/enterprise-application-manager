from django.urls import URLPattern, path

from core.views.database_size import (
    database_size_view,
    database_vacuum_action,
    database_snapshot_action,
    database_cleanup_historical_action,
)

urlpatterns_database_size: list[URLPattern] = [
    path(route='database-size/', view=database_size_view, name='database_size'),
    path(route='database-size/vacuum/', view=database_vacuum_action, name='database_vacuum'),
    path(route='database-size/snapshot/', view=database_snapshot_action, name='database_snapshot'),
    path(route='database-size/cleanup-historical/', view=database_cleanup_historical_action, name='database_cleanup_historical'),
]
