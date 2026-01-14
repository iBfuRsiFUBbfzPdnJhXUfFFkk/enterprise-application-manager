"""
Encryption health check endpoint view.

Provides a JSON endpoint at /authenticated/health/encryption/ that returns:
- Status: "healthy", "warning", or "error"
- Encryption key validation status
- Sample database statistics
- Legacy format warnings
- Timestamp

Requires staff user authentication for security.
"""

import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from core.utilities.encryption_health_check import get_encryption_status

logger = logging.getLogger(__name__)


def is_staff_user(user):
    """Check if user is staff member"""
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def encryption_health_view(request):
    """
    Health check endpoint for encryption system.

    GET /authenticated/health/encryption/

    Returns JSON with comprehensive encryption status.
    Requires staff user authentication.

    Response format:
    {
        "status": "healthy"|"warning"|"error",
        "encryption_key": "valid"|"invalid",
        "roundtrip_test": "passed"|"failed",
        "database_sample": {
            "total_encrypted_fields": int,
            "v1_format": int,
            "legacy_format": int,
            "failed_decryption": int
        },
        "warnings": [list of warning messages],
        "timestamp": "ISO8601 timestamp"
    }
    """
    try:
        status_report = get_encryption_status()

        # Determine HTTP status code based on health status
        if status_report['status'] == 'error':
            http_status = 500
        elif status_report['status'] == 'warning':
            http_status = 200  # Still return 200, but with warnings
        else:
            http_status = 200

        logger.info(
            f"Encryption health check accessed by user {request.user.username}: "
            f"status={status_report['status']}"
        )

        return JsonResponse(status_report, status=http_status)

    except Exception as e:
        logger.error(f"Encryption health check failed with unexpected error: {e}")
        return JsonResponse({
            'status': 'error',
            'encryption_key': 'unknown',
            'roundtrip_test': 'failed',
            'database_sample': {},
            'warnings': [f'Health check failed with error: {str(e)}'],
            'timestamp': None
        }, status=500)
