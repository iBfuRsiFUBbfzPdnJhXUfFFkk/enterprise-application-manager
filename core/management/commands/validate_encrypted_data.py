"""
Django management command to validate all encrypted data in the database.

This command scans all models with encrypted fields and validates:
- Encryption key is correct
- Data can be decrypted
- Format validation (v1 vs legacy)
- Identifies any corruption or issues

Usage:
    python manage.py validate_encrypted_data
    python manage.py validate_encrypted_data --verbose
    python manage.py validate_encrypted_data --fix  # Re-encrypt legacy format to v1
"""

from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models.database import Database
from core.models.login_credential import LoginCredential
from core.models.secret import Secret
from core.utilities.encryption import (
    InvalidEncryptionKeyError,
    CorruptedDataError,
    DecryptionFailureError,
    detect_encryption_format,
    decrypt_secret,
    encrypt_secret,
)


class Command(BaseCommand):
    help = 'Validate all encrypted data in the database and report issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output for each field',
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Re-encrypt legacy format data to v1 format',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        fix_legacy = options['fix']

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Encrypted Data Validation Report'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        total_fields = 0
        v1_count = 0
        legacy_count = 0
        failed_count = 0
        fixed_count = 0

        # Validate Secret models
        self.stdout.write(self.style.WARNING('Scanning Secret models...'))
        secrets = Secret.objects.exclude(Q(encrypted_value__isnull=True) | Q(encrypted_value=''))
        for secret in secrets:
            total_fields += 1
            result = self._validate_field(
                model_name='Secret',
                instance_id=secret.id,
                instance_name=str(secret),
                field_name='encrypted_value',
                encrypted_value=secret.encrypted_value,
                verbose=verbose
            )

            if result['format'] == 'v1':
                v1_count += 1
            elif result['format'] == 'legacy':
                legacy_count += 1
                if fix_legacy and result['valid']:
                    # Re-encrypt to v1 format
                    try:
                        decrypted = decrypt_secret(secret.encrypted_value)
                        secret.set_encrypted_value(decrypted)
                        secret.save()
                        fixed_count += 1
                        if verbose:
                            self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))

            if not result['valid']:
                failed_count += 1

        # Validate LoginCredential models
        self.stdout.write(self.style.WARNING('Scanning LoginCredential models...'))
        credentials = LoginCredential.objects.exclude(Q(encrypted_password__isnull=True) | Q(encrypted_password=''))
        for credential in credentials:
            total_fields += 1
            result = self._validate_field(
                model_name='LoginCredential',
                instance_id=credential.id,
                instance_name=str(credential),
                field_name='encrypted_password',
                encrypted_value=credential.encrypted_password,
                verbose=verbose
            )

            if result['format'] == 'v1':
                v1_count += 1
            elif result['format'] == 'legacy':
                legacy_count += 1
                if fix_legacy and result['valid']:
                    try:
                        decrypted = decrypt_secret(credential.encrypted_password)
                        credential.set_encrypted_password(decrypted)
                        credential.save()
                        fixed_count += 1
                        if verbose:
                            self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))

            if not result['valid']:
                failed_count += 1

        # Validate Database models (4 encrypted fields)
        self.stdout.write(self.style.WARNING('Scanning Database models...'))
        databases = Database.objects.all()
        for database in databases:
            # Check encrypted_password
            if database.encrypted_password:
                total_fields += 1
                result = self._validate_field(
                    model_name='Database',
                    instance_id=database.id,
                    instance_name=str(database),
                    field_name='encrypted_password',
                    encrypted_value=database.encrypted_password,
                    verbose=verbose
                )
                if result['format'] == 'v1':
                    v1_count += 1
                elif result['format'] == 'legacy':
                    legacy_count += 1
                    if fix_legacy and result['valid']:
                        try:
                            decrypted = decrypt_secret(database.encrypted_password)
                            database.set_encrypted_password(decrypted)
                            database.save()
                            fixed_count += 1
                            if verbose:
                                self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))
                if not result['valid']:
                    failed_count += 1

            # Check encrypted_username
            if database.encrypted_username:
                total_fields += 1
                result = self._validate_field(
                    model_name='Database',
                    instance_id=database.id,
                    instance_name=str(database),
                    field_name='encrypted_username',
                    encrypted_value=database.encrypted_username,
                    verbose=verbose
                )
                if result['format'] == 'v1':
                    v1_count += 1
                elif result['format'] == 'legacy':
                    legacy_count += 1
                    if fix_legacy and result['valid']:
                        try:
                            decrypted = decrypt_secret(database.encrypted_username)
                            database.set_encrypted_username(decrypted)
                            database.save()
                            fixed_count += 1
                            if verbose:
                                self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))
                if not result['valid']:
                    failed_count += 1

            # Check encrypted_ssh_tunnel_username
            if database.encrypted_ssh_tunnel_username:
                total_fields += 1
                result = self._validate_field(
                    model_name='Database',
                    instance_id=database.id,
                    instance_name=str(database),
                    field_name='encrypted_ssh_tunnel_username',
                    encrypted_value=database.encrypted_ssh_tunnel_username,
                    verbose=verbose
                )
                if result['format'] == 'v1':
                    v1_count += 1
                elif result['format'] == 'legacy':
                    legacy_count += 1
                    if fix_legacy and result['valid']:
                        try:
                            decrypted = decrypt_secret(database.encrypted_ssh_tunnel_username)
                            database.set_encrypted_ssh_tunnel_username(decrypted)
                            database.save()
                            fixed_count += 1
                            if verbose:
                                self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))
                if not result['valid']:
                    failed_count += 1

            # Check encrypted_ssh_tunnel_password
            if database.encrypted_ssh_tunnel_password:
                total_fields += 1
                result = self._validate_field(
                    model_name='Database',
                    instance_id=database.id,
                    instance_name=str(database),
                    field_name='encrypted_ssh_tunnel_password',
                    encrypted_value=database.encrypted_ssh_tunnel_password,
                    verbose=verbose
                )
                if result['format'] == 'v1':
                    v1_count += 1
                elif result['format'] == 'legacy':
                    legacy_count += 1
                    if fix_legacy and result['valid']:
                        try:
                            decrypted = decrypt_secret(database.encrypted_ssh_tunnel_password)
                            database.set_encrypted_ssh_tunnel_password(decrypted)
                            database.save()
                            fixed_count += 1
                            if verbose:
                                self.stdout.write(self.style.SUCCESS(f'  ✓ Re-encrypted to v1 format'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ✗ Failed to re-encrypt: {e}'))
                if not result['valid']:
                    failed_count += 1

        # Summary report
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Summary'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'Total encrypted fields scanned: {total_fields}')
        self.stdout.write(f'v1 format (with validation): {v1_count}')
        self.stdout.write(f'Legacy format: {legacy_count}')
        if fix_legacy:
            self.stdout.write(self.style.SUCCESS(f'Fields re-encrypted to v1: {fixed_count}'))

        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f'Failed decryption: {failed_count}'))
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('⚠ CRITICAL: Some fields failed to decrypt!'))
            self.stdout.write(self.style.ERROR('This likely indicates:'))
            self.stdout.write(self.style.ERROR('  1. Wrong ENCRYPTION_SECRET environment variable'))
            self.stdout.write(self.style.ERROR('  2. Corrupted encrypted data'))
            self.stdout.write('')
        else:
            self.stdout.write(self.style.SUCCESS(f'Failed decryption: {failed_count}'))

        # Recommendations
        if legacy_count > 0 and not fix_legacy:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('ℹ Note: Legacy format fields will be upgraded to v1 on next save.'))
            self.stdout.write(self.style.WARNING('   To force re-encryption now, run with --fix flag:'))
            self.stdout.write(self.style.WARNING('   python manage.py validate_encrypted_data --fix'))

        self.stdout.write('')
        if failed_count == 0:
            self.stdout.write(self.style.SUCCESS('✓ All encrypted data validated successfully!'))
        else:
            self.stdout.write(self.style.ERROR('✗ Validation completed with errors.'))

    def _validate_field(self, model_name, instance_id, instance_name, field_name, encrypted_value, verbose):
        """
        Validate a single encrypted field.

        Returns dict with:
            - valid: bool
            - format: 'v1' or 'legacy'
            - error: str or None
        """
        result = {
            'valid': False,
            'format': None,
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
                if verbose:
                    self.stdout.write(
                        f'  ✓ {model_name} id={instance_id} ({instance_name}) - '
                        f'{field_name} - {format_type} format - OK'
                    )
            else:
                result['error'] = 'Decryption returned None'
                self.stdout.write(self.style.ERROR(
                    f'  ✗ {model_name} id={instance_id} ({instance_name}) - '
                    f'{field_name} - Decryption failed (returned None)'
                ))

        except InvalidEncryptionKeyError as e:
            result['error'] = f'Invalid encryption key: {e}'
            self.stdout.write(self.style.ERROR(
                f'  ✗ {model_name} id={instance_id} ({instance_name}) - '
                f'{field_name} - INVALID ENCRYPTION KEY'
            ))
            if verbose:
                self.stdout.write(self.style.ERROR(f'     Error: {e}'))

        except CorruptedDataError as e:
            result['error'] = f'Corrupted data: {e}'
            self.stdout.write(self.style.ERROR(
                f'  ✗ {model_name} id={instance_id} ({instance_name}) - '
                f'{field_name} - CORRUPTED DATA'
            ))
            if verbose:
                self.stdout.write(self.style.ERROR(f'     Error: {e}'))

        except DecryptionFailureError as e:
            result['error'] = f'Decryption failure: {e}'
            self.stdout.write(self.style.ERROR(
                f'  ✗ {model_name} id={instance_id} ({instance_name}) - '
                f'{field_name} - DECRYPTION FAILED'
            ))
            if verbose:
                self.stdout.write(self.style.ERROR(f'     Error: {e}'))

        except Exception as e:
            result['error'] = f'Unexpected error: {e}'
            self.stdout.write(self.style.ERROR(
                f'  ✗ {model_name} id={instance_id} ({instance_name}) - '
                f'{field_name} - UNEXPECTED ERROR'
            ))
            if verbose:
                self.stdout.write(self.style.ERROR(f'     Error: {e}'))

        return result
