"""
Management command to migrate blob data from database to MinIO object storage.

This command implements a safe, incremental migration strategy with multiple
verification levels to prevent data loss.

Usage:
    python manage.py migrate_to_minio [--dry-run] [--verify] [--model=ModelName] [--batch-size=100]

Examples:
    # Dry run to see what would be migrated
    python manage.py migrate_to_minio --dry-run

    # Migrate all files with verification
    python manage.py migrate_to_minio

    # Migrate only Document model
    python manage.py migrate_to_minio --model=Document

    # Verify existing migration
    python manage.py migrate_to_minio --verify

    # Custom batch size
    python manage.py migrate_to_minio --batch-size=50
"""

import hashlib
import io
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.db import transaction
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate blob data from database to MinIO object storage'

    def __init__(self):
        super().__init__()
        self.stats = {
            'total': 0,
            'migrated': 0,
            'skipped': 0,
            'failed': 0,
            'total_size': 0,
            'errors': []
        }

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify existing migration instead of migrating',
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Migrate only a specific model (Document, BadInteraction, etc.)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to process in each batch (default: 100)',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.verify_only = options['verify']
        self.batch_size = options['batch_size']

        if not settings.USE_MINIO:
            raise CommandError(
                'MinIO is not enabled. Set USE_MINIO=true in your .env file.'
            )

        # Get models to process
        models_to_process = self._get_models_to_process(options.get('model'))

        if not models_to_process:
            raise CommandError('No models found with dual-storage support')

        # Display header
        mode = 'VERIFICATION' if self.verify_only else ('DRY RUN' if self.dry_run else 'MIGRATION')
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 80}'))
        self.stdout.write(self.style.SUCCESS(f'MinIO Migration Tool - {mode} Mode'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 80}\n'))

        # Process each model
        for model in models_to_process:
            if self.verify_only:
                self._verify_model(model)
            else:
                self._migrate_model(model)

        # Display summary
        self._display_summary()

    def _get_models_to_process(self, model_name=None):
        """Get list of models that support dual-storage migration."""
        # Models with dual-storage pattern
        model_configs = [
            ('core', 'Document'),
            ('core', 'BadInteraction'),
            ('core', 'BadInteractionUpdate'),
            ('core', 'HRIncidentUpdate'),
        ]

        models = []
        for app_label, model_class_name in model_configs:
            if model_name and model_class_name != model_name:
                continue
            try:
                model = apps.get_model(app_label, model_class_name)
                # Verify model has required fields (any blob field variant)
                has_blob_field = (
                    hasattr(model, 'blob_data') or
                    hasattr(model, 'evidence_blob_data') or
                    hasattr(model, 'attachment_blob_data')
                )
                if has_blob_field and hasattr(model, 'migrated_to_minio'):
                    models.append(model)
            except LookupError:
                pass

        return models

    def _get_file_field_name(self, model):
        """Get the name of the FileField for this model."""
        if hasattr(model, 'file'):
            return 'file'
        elif hasattr(model, 'evidence_file'):
            return 'evidence_file'
        elif hasattr(model, 'attachment_file'):
            return 'attachment_file'
        return None

    def _get_blob_field_name(self, model):
        """Get the name of the blob data field for this model."""
        if hasattr(model, 'blob_data'):
            return 'blob_data'
        elif hasattr(model, 'evidence_blob_data'):
            return 'evidence_blob_data'
        elif hasattr(model, 'attachment_blob_data'):
            return 'attachment_blob_data'
        return None

    def _get_blob_filename_field_name(self, model):
        """Get the name of the blob filename field for this model."""
        if hasattr(model, 'blob_filename'):
            return 'blob_filename'
        elif hasattr(model, 'evidence_blob_filename'):
            return 'evidence_blob_filename'
        elif hasattr(model, 'attachment_blob_filename'):
            return 'attachment_blob_filename'
        return None

    def _get_blob_size_field_name(self, model):
        """Get the name of the blob size field for this model."""
        if hasattr(model, 'blob_size'):
            return 'blob_size'
        elif hasattr(model, 'evidence_blob_size'):
            return 'evidence_blob_size'
        elif hasattr(model, 'attachment_blob_size'):
            return 'attachment_blob_size'
        return None

    def _migrate_model(self, model):
        """Migrate blob data to MinIO for a specific model."""
        model_name = model.__name__
        self.stdout.write(f'\nProcessing {model_name}...')

        # Get the blob field name for this model
        blob_field_name = self._get_blob_field_name(model)
        if not blob_field_name:
            self.stdout.write(self.style.WARNING(f'  No blob field found for {model_name}'))
            return

        # Get records that need migration
        filter_kwargs = {
            'migrated_to_minio': False,
            f'{blob_field_name}__isnull': False
        }
        exclude_kwargs = {blob_field_name: b''}
        queryset = model.objects.filter(**filter_kwargs).exclude(**exclude_kwargs)

        total_count = queryset.count()

        if total_count == 0:
            self.stdout.write(self.style.WARNING(f'  No records to migrate for {model_name}'))
            return

        self.stdout.write(f'  Found {total_count} records to migrate')

        if self.dry_run:
            self._display_dry_run_info(queryset, model_name)
            return

        # Process in batches
        processed = 0
        for i in range(0, total_count, self.batch_size):
            batch = queryset[i:i + self.batch_size]
            self._process_batch(batch, model, model_name, processed, total_count)
            processed += len(batch)

    def _process_batch(self, batch, model, model_name, processed, total):
        """Process a batch of records."""
        file_field_name = self._get_file_field_name(model)
        blob_field_name = self._get_blob_field_name(model)
        blob_filename_field_name = self._get_blob_filename_field_name(model)
        blob_size_field_name = self._get_blob_size_field_name(model)

        for obj in batch:
            try:
                with transaction.atomic():
                    # Get blob data
                    blob_data = getattr(obj, blob_field_name)
                    blob_filename = getattr(obj, blob_filename_field_name)
                    blob_size = getattr(obj, blob_size_field_name, 0)

                    # Create ContentFile from blob data
                    content = ContentFile(blob_data)

                    # Save to FileField
                    file_field = getattr(obj, file_field_name)
                    file_field.save(blob_filename, content, save=False)

                    # Mark as migrated
                    obj.migrated_to_minio = True
                    obj.save()

                    # Update stats
                    self.stats['migrated'] += 1
                    self.stats['total_size'] += blob_size or 0

                    # Progress indicator (every 10 files)
                    if self.stats['migrated'] % 10 == 0:
                        progress = ((processed + self.stats['migrated']) / total) * 100
                        self.stdout.write(
                            f'  Progress: {progress:.1f}% '
                            f'({processed + self.stats["migrated"]}/{total}) - '
                            f'Latest: {blob_filename}'
                        )

            except Exception as e:
                self.stats['failed'] += 1
                error_msg = f'{model_name} ID {obj.pk}: {str(e)}'
                self.stats['errors'].append(error_msg)
                self.stdout.write(self.style.ERROR(f'  ERROR: {error_msg}'))

    def _display_dry_run_info(self, queryset, model_name):
        """Display information about what would be migrated."""
        if queryset.count() == 0:
            return

        model = queryset.model
        blob_filename_field_name = self._get_blob_filename_field_name(model)
        blob_size_field_name = self._get_blob_size_field_name(model)

        total_size = sum(getattr(obj, blob_size_field_name, 0) or 0 for obj in queryset)

        self.stdout.write(f'  Would migrate {queryset.count()} records')
        self.stdout.write(f'  Total size: {self._format_bytes(total_size)}')

        # Show first 5 examples
        self.stdout.write(f'\n  Examples:')
        for obj in queryset[:5]:
            blob_filename = getattr(obj, blob_filename_field_name, 'unknown')
            blob_size = getattr(obj, blob_size_field_name, 0) or 0
            size_str = self._format_bytes(blob_size)
            self.stdout.write(f'    - ID {obj.pk}: {blob_filename} ({size_str})')

        if queryset.count() > 5:
            self.stdout.write(f'    ... and {queryset.count() - 5} more')

        self.stats['total'] += queryset.count()

    def _verify_model(self, model):
        """Verify migration for a specific model."""
        model_name = model.__name__
        self.stdout.write(f'\nVerifying {model_name}...')

        file_field_name = self._get_file_field_name(model)
        blob_field_name = self._get_blob_field_name(model)
        blob_size_field_name = self._get_blob_size_field_name(model)

        # Get migrated records
        migrated = model.objects.filter(migrated_to_minio=True)
        migrated_count = migrated.count()

        if migrated_count == 0:
            self.stdout.write(self.style.WARNING(f'  No migrated records for {model_name}'))
            return

        self.stdout.write(f'  Found {migrated_count} migrated records')

        # Verification levels
        passed = {
            'count': 0,
            'size': 0,
            'checksum': 0,
            'download': 0
        }
        failed = {
            'count': 0,
            'size': 0,
            'checksum': 0,
            'download': 0
        }

        for obj in migrated:
            # Level 1: File exists
            file_field = getattr(obj, file_field_name)
            if file_field:
                passed['count'] += 1

                # Get blob size for this object
                blob_size = getattr(obj, blob_size_field_name, None)

                # Level 2: Size verification
                try:
                    if file_field.size == blob_size:
                        passed['size'] += 1
                    else:
                        failed['size'] += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'  Size mismatch for ID {obj.pk}: '
                                f'MinIO={file_field.size} vs blob={blob_size}'
                            )
                        )
                except Exception as e:
                    failed['size'] += 1
                    self.stdout.write(
                        self.style.ERROR(f'  Size check failed for ID {obj.pk}: {e}')
                    )

                # Level 3: Checksum verification (if blob still exists)
                blob_data = getattr(obj, blob_field_name, None)
                if blob_data:
                    try:
                        blob_md5 = hashlib.md5(blob_data).hexdigest()
                        file_field.open('rb')
                        minio_md5 = hashlib.md5(file_field.read()).hexdigest()
                        file_field.close()

                        if blob_md5 == minio_md5:
                            passed['checksum'] += 1
                        else:
                            failed['checksum'] += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  Checksum mismatch for ID {obj.pk}'
                                )
                            )
                    except Exception as e:
                        failed['checksum'] += 1
                        self.stdout.write(
                            self.style.ERROR(f'  Checksum failed for ID {obj.pk}: {e}')
                        )

                # Level 4: Download test
                try:
                    file_field.open('rb')
                    data = file_field.read()
                    file_field.close()
                    if len(data) > 0:
                        passed['download'] += 1
                    else:
                        failed['download'] += 1
                except Exception as e:
                    failed['download'] += 1
                    self.stdout.write(
                        self.style.ERROR(f'  Download test failed for ID {obj.pk}: {e}')
                    )
            else:
                failed['count'] += 1
                self.stdout.write(
                    self.style.ERROR(f'  File missing for ID {obj.pk}')
                )

        # Display verification results
        self.stdout.write(f'\n  Verification Results:')
        self._display_verification_result('File count', passed['count'], failed['count'])
        self._display_verification_result('Size verification', passed['size'], failed['size'])
        if passed['checksum'] > 0 or failed['checksum'] > 0:
            self._display_verification_result('Checksum verification', passed['checksum'], failed['checksum'])
        self._display_verification_result('Download test', passed['download'], failed['download'])

    def _display_verification_result(self, name, passed, failed):
        """Display a verification result line."""
        total = passed + failed
        if total == 0:
            status = self.style.WARNING('SKIP')
            detail = 'No data to verify'
        elif failed == 0:
            status = self.style.SUCCESS('PASS')
            detail = f'{passed}/{total}'
        else:
            status = self.style.ERROR('FAIL')
            detail = f'{passed}/{total} (failed: {failed})'

        self.stdout.write(f'    {name:.<40} {status} {detail}')

    def _display_summary(self):
        """Display migration summary."""
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 80}'))
        self.stdout.write(self.style.SUCCESS('Summary'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 80}\n'))

        if not self.verify_only:
            self.stdout.write(f'  Total records processed: {self.stats["total"]}')
            self.stdout.write(f'  Successfully migrated:   {self.stats["migrated"]}')
            self.stdout.write(f'  Failed:                  {self.stats["failed"]}')
            self.stdout.write(f'  Total size migrated:     {self._format_bytes(self.stats["total_size"])}')

            if self.stats['errors']:
                self.stdout.write(self.style.ERROR(f'\n  Errors:'))
                for error in self.stats['errors']:
                    self.stdout.write(self.style.ERROR(f'    - {error}'))

            if self.stats['migrated'] > 0 and self.stats['failed'] == 0:
                self.stdout.write(self.style.SUCCESS('\n  ✓ Migration completed successfully!'))
                if not self.dry_run:
                    self.stdout.write(self.style.SUCCESS('  Run with --verify to verify the migration'))

    @staticmethod
    def _format_bytes(bytes_value):
        """Format bytes into human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f'{bytes_value:.2f} {unit}'
            bytes_value /= 1024.0
        return f'{bytes_value:.2f} TB'
