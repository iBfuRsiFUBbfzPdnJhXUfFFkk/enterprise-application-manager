from typing import Mapping, Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db import connection, transaction
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from datetime import timedelta
from collections import defaultdict
from django.apps import apps
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
    cutoff_date = timezone.now() - timedelta(days=days)
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


def get_historical_models() -> list[dict[str, Any]]:
    """
    Get all historical models (from django-simple-history).
    Returns a list of dicts with model info.
    """
    historical_models = []

    for model in apps.get_models():
        model_name = model.__name__
        # Check if this is a historical model from django-simple-history
        if model_name.startswith('Historical'):
            # Get the table name
            table_name = model._meta.db_table

            # Get count of records
            try:
                count = model.objects.count()
            except Exception:
                count = 0

            historical_models.append({
                'model_name': model_name,
                'table_name': table_name,
                'record_count': count,
                'app_label': model._meta.app_label,
            })

    # Sort by record count descending
    historical_models.sort(key=lambda x: x['record_count'], reverse=True)

    return historical_models


def cleanup_historical_data(
    table_name: str | None = None,
    days_to_keep: int = 90
) -> dict[str, Any]:
    """
    Clean up old historical records from django-simple-history tables.

    Args:
        table_name: Specific table to clean (None = all historical tables)
        days_to_keep: Number of days of history to retain

    Returns:
        Dictionary with cleanup results
    """
    cutoff_date = timezone.now() - timedelta(days=days_to_keep)
    results = {
        'tables_processed': 0,
        'records_deleted': 0,
        'errors': [],
    }

    # Get all historical models or filter to specific table
    historical_models = get_historical_models()

    if table_name:
        # Filter to specific table
        historical_models = [
            m for m in historical_models
            if m['table_name'] == table_name
        ]

    # Clean up each historical table
    for model_info in historical_models:
        try:
            # Get the model class
            model = apps.get_model(
                model_info['app_label'],
                model_info['model_name']
            )

            # Delete old records
            # Historical models use 'history_date' field
            deleted_count, _ = model.objects.filter(
                history_date__lt=cutoff_date
            ).delete()

            results['tables_processed'] += 1
            results['records_deleted'] += deleted_count

        except Exception as e:
            results['errors'].append(
                f"Error cleaning {model_info['table_name']}: {str(e)}"
            )

    return results


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

    # Get historical models info
    historical_models = get_historical_models()

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
        'historical_models': historical_models,
        'historical_models_json': json.dumps(historical_models),
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

    Note: VACUUM must run outside of a transaction in SQLite.
    """
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    try:
        # Set autocommit mode to ensure VACUUM runs outside a transaction
        old_autocommit = transaction.get_autocommit()
        transaction.set_autocommit(True)

        try:
            with connection.cursor() as cursor:
                # Get size before vacuum
                cursor.execute("PRAGMA page_count")
                pages_before = cursor.fetchone()[0]
                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]
                size_before = pages_before * page_size

                # Perform VACUUM (must be outside transaction)
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
        finally:
            # Restore original autocommit setting
            transaction.set_autocommit(old_autocommit)

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


@login_required
@require_http_methods(["POST"])
def database_cleanup_historical_action(request: HttpRequest) -> JsonResponse:
    """
    Clean up old historical records from django-simple-history tables.
    Only accessible to superusers.
    """
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    try:
        # Parse request body for parameters
        data = json.loads(request.body) if request.body else {}
        table_name = data.get('table_name', None)
        days_to_keep = int(data.get('days_to_keep', 90))

        # Validate days_to_keep
        if days_to_keep < 1:
            return JsonResponse({
                'success': False,
                'error': 'days_to_keep must be at least 1'
            }, status=400)

        # Perform cleanup
        results = cleanup_historical_data(
            table_name=table_name,
            days_to_keep=days_to_keep
        )

        return JsonResponse({
            'success': True,
            'tables_processed': results['tables_processed'],
            'records_deleted': results['records_deleted'],
            'errors': results['errors'],
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
