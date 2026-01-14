"""
Encryption health check utility for monitoring encryption system status.

Provides functions to:
- Test encryption/decryption round-trip
- Validate ENCRYPTION_SECRET is correct
- Scan sample encrypted data in database
- Return comprehensive health status
"""

import logging
from datetime import datetime
from typing import Dict, Any

from django.db.models import Q

from core.models.database import Database
from core.models.login_credential import LoginCredential
from core.models.secret import Secret
from core.utilities.encryption import (
    encrypt_secret,
    decrypt_secret,
    detect_encryption_format,
    InvalidEncryptionKeyError,
    DecryptionFailureError,
)

logger = logging.getLogger(__name__)


def test_encryption_roundtrip() -> Dict[str, Any]:
    """
    Test encryption/decryption round-trip with a test string.

    Returns:
        dict with 'passed' (bool) and 'error' (str or None)
    """
    test_string = "test_encryption_health_check_2026"

    try:
        # Encrypt
        encrypted = encrypt_secret(test_string)
        if not encrypted:
            return {'passed': False, 'error': 'Encryption returned None'}

        # Verify it's in v1 format
        if not encrypted.startswith('v1:'):
            return {'passed': False, 'error': f'Encryption did not produce v1 format: {encrypted[:20]}...'}

        # Decrypt
        decrypted = decrypt_secret(encrypted)
        if decrypted != test_string:
            return {'passed': False, 'error': f'Decryption mismatch: expected "{test_string}", got "{decrypted}"'}

        return {'passed': True, 'error': None}

    except Exception as e:
        logger.error(f"Encryption round-trip test failed: {e}")
        return {'passed': False, 'error': str(e)}


def validate_encryption_key() -> Dict[str, Any]:
    """
    Validate that ENCRYPTION_SECRET is set correctly by testing round-trip.

    Returns:
        dict with 'valid' (bool), 'error' (str or None)
    """
    result = test_encryption_roundtrip()

    if result['passed']:
        return {'valid': True, 'error': None}
    else:
        return {'valid': False, 'error': result['error']}


def scan_encrypted_data(sample_size: int = 10) -> Dict[str, Any]:
    """
    Scan a sample of encrypted data in the database and return statistics.

    Args:
        sample_size: Number of records to check per model (default: 10)

    Returns:
        dict with statistics about encrypted data
    """
    stats = {
        'total_encrypted_fields': 0,
        'v1_format': 0,
        'legacy_format': 0,
        'failed_decryption': 0,
        'sample_size': sample_size,
        'errors': []
    }

    # Sample Secret models
    secrets = Secret.objects.exclude(Q(encrypted_value__isnull=True) | Q(encrypted_value=''))[:sample_size]
    for secret in secrets:
        stats['total_encrypted_fields'] += 1
        result = _check_field(secret.encrypted_value, f'Secret id={secret.id}')
        _update_stats(stats, result)

    # Sample LoginCredential models
    credentials = LoginCredential.objects.exclude(
        Q(encrypted_password__isnull=True) | Q(encrypted_password='')
    )[:sample_size]
    for credential in credentials:
        stats['total_encrypted_fields'] += 1
        result = _check_field(credential.encrypted_password, f'LoginCredential id={credential.id}')
        _update_stats(stats, result)

    # Sample Database models (check all 4 encrypted fields)
    databases = Database.objects.all()[:sample_size]
    for database in databases:
        if database.encrypted_password:
            stats['total_encrypted_fields'] += 1
            result = _check_field(database.encrypted_password, f'Database id={database.id} (password)')
            _update_stats(stats, result)

        if database.encrypted_username:
            stats['total_encrypted_fields'] += 1
            result = _check_field(database.encrypted_username, f'Database id={database.id} (username)')
            _update_stats(stats, result)

        if database.encrypted_ssh_tunnel_username:
            stats['total_encrypted_fields'] += 1
            result = _check_field(database.encrypted_ssh_tunnel_username, f'Database id={database.id} (ssh_user)')
            _update_stats(stats, result)

        if database.encrypted_ssh_tunnel_password:
            stats['total_encrypted_fields'] += 1
            result = _check_field(database.encrypted_ssh_tunnel_password, f'Database id={database.id} (ssh_pass)')
            _update_stats(stats, result)

    return stats


def _check_field(encrypted_value: str, field_description: str) -> Dict[str, Any]:
    """
    Check a single encrypted field.

    Returns:
        dict with 'format', 'valid', 'error'
    """
    result = {
        'format': None,
        'valid': False,
        'error': None
    }

    try:
        # Detect format
        format_type = detect_encryption_format(encrypted_value)
        result['format'] = format_type

        # Try to decrypt
        decrypted = decrypt_secret(encrypted_value)

        if decrypted is not None:
            result['valid'] = True
        else:
            result['error'] = f'{field_description}: Decryption returned None'

    except (InvalidEncryptionKeyError, DecryptionFailureError) as e:
        result['error'] = f'{field_description}: {type(e).__name__} - {str(e)}'
        logger.warning(f"Health check found decryption issue: {result['error']}")

    except Exception as e:
        result['error'] = f'{field_description}: Unexpected error - {str(e)}'
        logger.error(f"Health check unexpected error: {result['error']}")

    return result


def _update_stats(stats: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Update statistics dict based on field check result"""
    if result['format'] == 'v1':
        stats['v1_format'] += 1
    elif result['format'] == 'legacy':
        stats['legacy_format'] += 1

    if not result['valid']:
        stats['failed_decryption'] += 1

    if result['error']:
        stats['errors'].append(result['error'])


def get_encryption_status() -> Dict[str, Any]:
    """
    Get comprehensive encryption system health status.

    Returns:
        dict with:
        - status: 'healthy', 'warning', or 'error'
        - encryption_key: 'valid' or 'invalid'
        - roundtrip_test: 'passed' or 'failed'
        - database_sample: dict with statistics
        - warnings: list of warning messages
        - timestamp: ISO format timestamp
    """
    status_report = {
        'status': 'healthy',
        'encryption_key': 'valid',
        'roundtrip_test': 'passed',
        'database_sample': {},
        'warnings': [],
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    # Test round-trip
    roundtrip = test_encryption_roundtrip()
    if not roundtrip['passed']:
        status_report['roundtrip_test'] = 'failed'
        status_report['encryption_key'] = 'invalid'
        status_report['status'] = 'error'
        status_report['warnings'].append(f"Encryption round-trip failed: {roundtrip['error']}")
        return status_report

    # Scan database sample
    try:
        db_stats = scan_encrypted_data(sample_size=10)
        status_report['database_sample'] = {
            'total_encrypted_fields': db_stats['total_encrypted_fields'],
            'v1_format': db_stats['v1_format'],
            'legacy_format': db_stats['legacy_format'],
            'failed_decryption': db_stats['failed_decryption']
        }

        # Check for issues
        if db_stats['failed_decryption'] > 0:
            status_report['status'] = 'error'
            status_report['encryption_key'] = 'invalid'
            status_report['warnings'].append(
                f"{db_stats['failed_decryption']} fields failed to decrypt - "
                "ENCRYPTION_SECRET may be incorrect"
            )
            # Add error details
            for error in db_stats['errors'][:5]:  # Limit to first 5 errors
                status_report['warnings'].append(error)

        elif db_stats['legacy_format'] > 0:
            status_report['status'] = 'warning'
            status_report['warnings'].append(
                f"{db_stats['legacy_format']} fields using legacy encryption format "
                "(will upgrade on next save)"
            )

    except Exception as e:
        logger.error(f"Health check database scan failed: {e}")
        status_report['status'] = 'error'
        status_report['warnings'].append(f"Database scan failed: {str(e)}")

    return status_report
