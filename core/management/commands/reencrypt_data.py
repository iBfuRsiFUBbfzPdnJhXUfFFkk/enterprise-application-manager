"""
Django management command to re-encrypt all encrypted data with a new encryption key.

This command is used when rotating encryption keys. It decrypts all data with the current
key and re-encrypts it with a new key.

IMPORTANT: This command requires careful execution:
1. Decrypt all data with the OLD encryption key
2. Change ENCRYPTION_SECRET to the NEW key
3. Restart the application
4. Run this command to re-encrypt with the NEW key

Usage:
    # With confirmation prompt
    python manage.py reencrypt_data

    # Force re-encryption without prompt (use with caution!)
    python manage.py reencrypt_data --force

    # Dry run - show what would be re-encrypted
    python manage.py reencrypt_data --dry-run
"""

from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models.database import Database
from core.models.login_credential import LoginCredential
from core.models.secret import Secret
from core.utilities.encryption import (
    decrypt_secret,
    detect_encryption_format,
)


class Command(BaseCommand):
    help = 'Re-encrypt all encrypted data (useful for key rotation)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-encryption without confirmation prompt',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be re-encrypted without actually doing it',
        )

    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']

        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('Re-encryption Command'))
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write('')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
            self.stdout.write('')

        # Count fields to re-encrypt
        total_fields = self._count_encrypted_fields()

        self.stdout.write(f'Found {total_fields} encrypted fields to re-encrypt')
        self.stdout.write('')

        if total_fields == 0:
            self.stdout.write(self.style.SUCCESS('No encrypted fields found. Nothing to do.'))
            return

        # Confirmation prompt (unless --force or --dry-run)
        if not force and not dry_run:
            self.stdout.write(self.style.WARNING('⚠ WARNING: This will re-encrypt ALL encrypted data!'))
            self.stdout.write('')
            self.stdout.write('This command should be used when rotating encryption keys.')
            self.stdout.write('Make sure you have:')
            self.stdout.write('  1. Backed up your database')
            self.stdout.write('  2. Tested decryption with the current ENCRYPTION_SECRET')
            self.stdout.write('  3. Verified the new ENCRYPTION_SECRET is correct')
            self.stdout.write('')

            confirm = input('Are you sure you want to continue? Type "yes" to proceed: ')

            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Aborted.'))
                return

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Starting re-encryption...'))
        self.stdout.write('')

        success_count = 0
        error_count = 0

        # Re-encrypt Secret models
        self.stdout.write('Re-encrypting Secret models...')
        secrets = Secret.objects.exclude(Q(encrypted_value__isnull=True) | Q(encrypted_value=''))
        for secret in secrets:
            try:
                # Decrypt with current key
                decrypted = decrypt_secret(secret.encrypted_value)

                if decrypted is not None:
                    if not dry_run:
                        # Re-encrypt with current key (will use v1 format)
                        secret.set_encrypted_value(decrypted)
                        secret.save()
                    success_count += 1
                    self.stdout.write(f'  ✓ Secret id={secret.id} ({secret.name})')
                else:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Secret id={secret.id} - Decryption returned None'))
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Secret id={secret.id} - Error: {e}'))

        # Re-encrypt LoginCredential models
        self.stdout.write('')
        self.stdout.write('Re-encrypting LoginCredential models...')
        credentials = LoginCredential.objects.exclude(Q(encrypted_password__isnull=True) | Q(encrypted_password=''))
        for credential in credentials:
            try:
                decrypted = decrypt_secret(credential.encrypted_password)

                if decrypted is not None:
                    if not dry_run:
                        credential.set_encrypted_password(decrypted)
                        credential.save()
                    success_count += 1
                    self.stdout.write(f'  ✓ LoginCredential id={credential.id} ({credential.name})')
                else:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ LoginCredential id={credential.id} - Decryption returned None'))
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ LoginCredential id={credential.id} - Error: {e}'))

        # Re-encrypt Database models (4 fields each)
        self.stdout.write('')
        self.stdout.write('Re-encrypting Database models...')
        databases = Database.objects.all()
        for database in databases:
            # Process encrypted_password
            if database.encrypted_password:
                try:
                    decrypted = decrypt_secret(database.encrypted_password)
                    if decrypted is not None:
                        if not dry_run:
                            database.set_encrypted_password(decrypted)
                            database.save()
                        success_count += 1
                        self.stdout.write(f'  ✓ Database id={database.id} ({database.name}) - password')
                    else:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - password - Decryption returned None'))
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - password - Error: {e}'))

            # Process encrypted_username
            if database.encrypted_username:
                try:
                    decrypted = decrypt_secret(database.encrypted_username)
                    if decrypted is not None:
                        if not dry_run:
                            database.set_encrypted_username(decrypted)
                            database.save()
                        success_count += 1
                        self.stdout.write(f'  ✓ Database id={database.id} ({database.name}) - username')
                    else:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - username - Decryption returned None'))
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - username - Error: {e}'))

            # Process encrypted_ssh_tunnel_username
            if database.encrypted_ssh_tunnel_username:
                try:
                    decrypted = decrypt_secret(database.encrypted_ssh_tunnel_username)
                    if decrypted is not None:
                        if not dry_run:
                            database.set_encrypted_ssh_tunnel_username(decrypted)
                            database.save()
                        success_count += 1
                        self.stdout.write(f'  ✓ Database id={database.id} ({database.name}) - ssh_username')
                    else:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - ssh_username - Decryption returned None'))
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - ssh_username - Error: {e}'))

            # Process encrypted_ssh_tunnel_password
            if database.encrypted_ssh_tunnel_password:
                try:
                    decrypted = decrypt_secret(database.encrypted_ssh_tunnel_password)
                    if decrypted is not None:
                        if not dry_run:
                            database.set_encrypted_ssh_tunnel_password(decrypted)
                            database.save()
                        success_count += 1
                        self.stdout.write(f'  ✓ Database id={database.id} ({database.name}) - ssh_password')
                    else:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - ssh_password - Decryption returned None'))
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Database id={database.id} - ssh_password - Error: {e}'))

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Summary'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes were made'))
            self.stdout.write(f'Would re-encrypt: {success_count} fields')
            self.stdout.write(f'Would fail: {error_count} fields')
        else:
            self.stdout.write(f'Successfully re-encrypted: {success_count} fields')
            self.stdout.write(f'Failed: {error_count} fields')

        self.stdout.write('')

        if error_count > 0:
            self.stdout.write(self.style.ERROR('⚠ Some fields failed to re-encrypt!'))
            self.stdout.write(self.style.ERROR('Check the errors above and run validate_encrypted_data for details.'))
        else:
            if dry_run:
                self.stdout.write(self.style.SUCCESS('✓ Dry run completed successfully!'))
                self.stdout.write('')
                self.stdout.write('Run without --dry-run to perform actual re-encryption.')
            else:
                self.stdout.write(self.style.SUCCESS('✓ All fields re-encrypted successfully!'))

    def _count_encrypted_fields(self):
        """Count total number of encrypted fields across all models"""
        count = 0

        # Count Secret models
        count += Secret.objects.exclude(Q(encrypted_value__isnull=True) | Q(encrypted_value='')).count()

        # Count LoginCredential models
        count += LoginCredential.objects.exclude(Q(encrypted_password__isnull=True) | Q(encrypted_password='')).count()

        # Count Database models (4 fields each)
        databases = Database.objects.all()
        for db in databases:
            if db.encrypted_password:
                count += 1
            if db.encrypted_username:
                count += 1
            if db.encrypted_ssh_tunnel_username:
                count += 1
            if db.encrypted_ssh_tunnel_password:
                count += 1

        return count
