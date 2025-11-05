from typing import Mapping, Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from collections import defaultdict
import json

from core.models.database_size_history import DatabaseSizeHistory
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def get_table_sizes() -> list[dict[str, Any]]:
    """
    Query SQLite database to get table sizes, row counts, and index sizes.
    Returns a list of dictionaries with table statistics.
    """
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            AND name NOT LIKE 'django_session'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Get page size once
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]

        table_stats = []
        total_size = 0

        # Try to use dbstat if available, otherwise use a simpler approximation
        try:
            cursor.execute("SELECT 1 FROM dbstat LIMIT 1")
            use_dbstat = True
        except Exception:
            use_dbstat = False

        for table_name in tables:
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
            row_count = cursor.fetchone()[0]

            if use_dbstat:
                # Get table size using dbstat
                cursor.execute(
                    "SELECT SUM(pgsize) FROM dbstat WHERE name = %s",
                    [table_name]
                )
                result = cursor.fetchone()
                table_size = result[0] if result and result[0] else 0

                # Get index sizes
                cursor.execute(
                    """SELECT SUM(pgsize) FROM dbstat
                       WHERE name IN (
                           SELECT name FROM sqlite_master
                           WHERE type='index' AND tbl_name = %s
                       )""",
                    [table_name]
                )
                result = cursor.fetchone()
                index_size = result[0] if result and result[0] else 0
            else:
                # Estimate based on row count and average row size
                # This is a rough estimate when dbstat is not available
                table_size = row_count * 100  # Assume 100 bytes per row average
                index_size = row_count * 20   # Assume 20 bytes per index entry

            total_size += table_size + index_size

            table_stats.append({
                'table_name': table_name,
                'row_count': row_count,
                'size_bytes': table_size,
                'index_size_bytes': index_size,
                'total_bytes': table_size + index_size,
            })

        # Calculate percentages
        for stat in table_stats:
            stat['percentage'] = (stat['total_bytes'] / total_size * 100) if total_size > 0 else 0

        # Sort by total size descending
        table_stats.sort(key=lambda x: x['total_bytes'], reverse=True)

    return table_stats


def get_historical_data(days: int = 30) -> dict[str, list[dict[str, Any]]]:
    """
    Get historical size data for trend analysis.
    Returns data grouped by table name.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    history_records = DatabaseSizeHistory.objects.filter(
        recorded_at__gte=cutoff_date
    ).order_by('table_name', 'recorded_at')

    # Group by table name
    historical_data = defaultdict(list)
    for record in history_records:
        historical_data[record.table_name].append({
            'recorded_at': record.recorded_at.isoformat(),
            'size_bytes': record.size_bytes,
            'index_size_bytes': record.index_size_bytes,
            'total_bytes': record.size_bytes + record.index_size_bytes,
            'row_count': record.row_count,
        })

    return dict(historical_data)


def record_snapshot() -> int:
    """
    Record current database sizes as a snapshot.
    Returns the number of records created.
    """
    table_stats = get_table_sizes()
    created_count = 0

    for stat in table_stats:
        DatabaseSizeHistory.objects.create(
            table_name=stat['table_name'],
            size_bytes=stat['size_bytes'],
            index_size_bytes=stat['index_size_bytes'],
            row_count=stat['row_count'],
        )
        created_count += 1

    return created_count


@login_required
def database_size_view(request: HttpRequest) -> HttpResponse:
    """
    Display database size information with tables, charts, and trends.
    Only accessible to superusers.
    """
    # Check if user is superuser
    if not request.user.is_superuser:
        return generic_500(request=request)

    # Get current table sizes
    table_stats = get_table_sizes()

    # Get historical data for trends
    historical_data = get_historical_data(days=30)

    # Calculate total database size
    total_size = sum(stat['total_bytes'] for stat in table_stats)

    # Get database file size
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        db_file_size = page_count * page_size

    context: Mapping[str, Any] = {
        'table_stats': table_stats,
        'table_stats_json': json.dumps(table_stats),
        'historical_data_json': json.dumps(historical_data),
        'total_size': total_size,
        'db_file_size': db_file_size,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/database_size/database_size.html'
    )


@login_required
@require_http_methods(["POST"])
def database_vacuum_action(request: HttpRequest) -> JsonResponse:
    """
    Perform VACUUM operation on the database.
    Only accessible to superusers.
    """
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    try:
        with connection.cursor() as cursor:
            # Get size before vacuum
            cursor.execute("PRAGMA page_count")
            pages_before = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            size_before = pages_before * page_size

            # Perform VACUUM
            cursor.execute("VACUUM")

            # Get size after vacuum
            cursor.execute("PRAGMA page_count")
            pages_after = cursor.fetchone()[0]
            size_after = pages_after * page_size

            space_freed = size_before - size_after

        return JsonResponse({
            'success': True,
            'size_before': size_before,
            'size_after': size_after,
            'space_freed': space_freed,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def database_snapshot_action(request: HttpRequest) -> JsonResponse:
    """
    Record a snapshot of current database sizes.
    Only accessible to superusers.
    """
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    try:
        count = record_snapshot()
        return JsonResponse({
            'success': True,
            'records_created': count,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
