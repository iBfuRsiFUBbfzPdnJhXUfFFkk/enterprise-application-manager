"""
Management command to check and optionally create the MinIO bucket.

This command ensures the required MinIO bucket exists and is accessible.
It's designed to run automatically during container startup.

Usage:
    python manage.py check_minio_bucket [--create-if-missing]

Examples:
    # Check if bucket exists
    python manage.py check_minio_bucket

    # Check and create bucket if it doesn't exist
    python manage.py check_minio_bucket --create-if-missing
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
from botocore.exceptions import ClientError


class Command(BaseCommand):
    help = 'Check MinIO bucket exists and optionally create it'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-if-missing',
            action='store_true',
            help='Create the bucket if it does not exist',
        )

    def handle(self, *args, **options):
        # Check if MinIO is enabled
        if not getattr(settings, 'USE_MINIO', False):
            self.stdout.write(self.style.WARNING('MinIO is disabled (USE_MINIO=False)'))
            return

        # Get MinIO configuration
        bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'enterprise-app-media')
        endpoint_url = getattr(settings, 'AWS_S3_ENDPOINT_URL', None)

        if not endpoint_url:
            self.stdout.write(self.style.WARNING('MinIO endpoint not configured'))
            return

        try:
            # Create S3 client
            s3_client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
                aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
                region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
            )

            # Check if bucket exists
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ MinIO bucket "{bucket_name}" exists and is accessible')
                )
                return

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')

                if error_code == '404':
                    # Bucket doesn't exist
                    if options['create_if_missing']:
                        self.stdout.write(
                            self.style.WARNING(f'Bucket "{bucket_name}" does not exist. Creating...')
                        )
                        try:
                            s3_client.create_bucket(Bucket=bucket_name)
                            self.stdout.write(
                                self.style.SUCCESS(f'✓ Bucket "{bucket_name}" created successfully')
                            )
                        except Exception as create_error:
                            self.stdout.write(
                                self.style.ERROR(f'✗ Failed to create bucket: {str(create_error)}')
                            )
                            raise
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'✗ Bucket "{bucket_name}" does not exist')
                        )
                        self.stdout.write(
                            'Run with --create-if-missing to create it automatically'
                        )
                elif error_code == '403':
                    self.stdout.write(
                        self.style.ERROR(f'✗ Access denied to bucket "{bucket_name}"')
                    )
                    self.stdout.write('Check your MinIO credentials')
                else:
                    raise

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error checking MinIO bucket: {str(e)}')
            )
            # Don't raise - allow container to start even if MinIO isn't ready yet
            return
