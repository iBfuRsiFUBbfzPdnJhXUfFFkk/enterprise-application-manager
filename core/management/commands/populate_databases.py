from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.application import Application
from core.models.database import Database
from core.models.common.enums.database_flavor_choices import (
    DATABASE_FLAVOR_MARIADB,
    DATABASE_FLAVOR_POSTGRESQL,
)
from core.models.common.enums.environment_choices import (
    ENVIRONMENT_DEVELOPMENT,
    ENVIRONMENT_PRODUCTION,
    ENVIRONMENT_STAGING,
)
from core.models.common.enums.data_storage_form_choices import (
    DATA_STORAGE_FORM_RELATIONAL,
    DATA_STORAGE_FORM_DOCUMENT,
)


class Command(BaseCommand):
    help = 'Populates the database with test Database records'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        with transaction.atomic():
            # Get applications to associate with databases
            applications = list(Application.objects.all()[:5])

            if not applications:
                self.stdout.write(self.style.WARNING(
                    'No applications found. Please run populate_test_data first.'
                ))
                return

            # Create test databases
            self.stdout.write('Creating database records...')
            self.create_databases(applications)

        self.stdout.write(self.style.SUCCESS('Database population complete!'))

    def create_databases(self, applications):
        """Create test database records"""
        databases_data = [
            {
                'application': applications[0] if len(applications) > 0 else None,
                'hostname': 'db-prod-01.example.com',
                'ip_v4_internal': '10.0.1.100',
                'port': 5432,
                'schema': 'customer_portal',
                'version': '15.2',
                'type_database_flavor': DATABASE_FLAVOR_POSTGRESQL,
                'type_environment': ENVIRONMENT_PRODUCTION,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'Production database for customer portal application',
                'username': 'cp_app_user',
                'password': 'prod_secure_password_123',
            },
            {
                'application': applications[0] if len(applications) > 0 else None,
                'hostname': 'db-staging-01.example.com',
                'ip_v4_internal': '10.0.2.100',
                'port': 5432,
                'schema': 'customer_portal_staging',
                'version': '15.2',
                'type_database_flavor': DATABASE_FLAVOR_POSTGRESQL,
                'type_environment': ENVIRONMENT_STAGING,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'Staging environment database for testing',
                'username': 'cp_stage_user',
                'password': 'staging_password_456',
            },
            {
                'application': applications[1] if len(applications) > 1 else None,
                'hostname': 'erp-db-prod.internal.example.com',
                'ip_v4_internal': '10.0.1.101',
                'port': 3306,
                'schema': 'erp_production',
                'version': '10.11',
                'type_database_flavor': DATABASE_FLAVOR_MARIADB,
                'type_environment': ENVIRONMENT_PRODUCTION,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'MariaDB production database for ERP system',
                'username': 'erp_prod_user',
                'password': 'erp_prod_secure_789',
            },
            {
                'application': applications[1] if len(applications) > 1 else None,
                'hostname': 'localhost',
                'ip_v4_internal': '127.0.0.1',
                'port': 3306,
                'schema': 'erp_dev',
                'version': '10.11',
                'type_database_flavor': DATABASE_FLAVOR_MARIADB,
                'type_environment': ENVIRONMENT_DEVELOPMENT,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'Local development database for ERP',
                'username': 'dev_user',
                'password': 'dev_password',
            },
            {
                'application': applications[2] if len(applications) > 2 else None,
                'hostname': 'mobile-db-prod.example.com',
                'ip_v4_internal': '10.0.1.102',
                'port': 5432,
                'schema': 'mobile_banking',
                'version': '16.0',
                'type_database_flavor': DATABASE_FLAVOR_POSTGRESQL,
                'type_environment': ENVIRONMENT_PRODUCTION,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'Production PostgreSQL database for mobile banking app',
                'username': 'mba_prod_user',
                'password': 'mobile_secure_password',
            },
            {
                'application': applications[3] if len(applications) > 3 else None,
                'hostname': 'sync-db.internal.example.com',
                'ip_v4_internal': '10.0.1.103',
                'port': 5432,
                'schema': 'data_sync',
                'version': '15.2',
                'type_database_flavor': DATABASE_FLAVOR_POSTGRESQL,
                'type_environment': ENVIRONMENT_PRODUCTION,
                'type_data_storage_form': DATA_STORAGE_FORM_DOCUMENT,
                'comment': 'Document store for sync service metadata',
                'username': 'sync_user',
                'password': 'sync_password_abc',
            },
            {
                'application': applications[4] if len(applications) > 4 else None,
                'hostname': 'legacy-reports-db.internal.example.com',
                'ip_v4_internal': '10.0.1.50',
                'port': 3306,
                'schema': 'legacy_reports',
                'version': '5.7',
                'type_database_flavor': DATABASE_FLAVOR_MARIADB,
                'type_environment': ENVIRONMENT_PRODUCTION,
                'type_data_storage_form': DATA_STORAGE_FORM_RELATIONAL,
                'comment': 'Old MariaDB database for legacy reporting system',
                'username': 'legacy_user',
                'password': 'old_password',
            },
        ]

        for db_data in databases_data:
            # Extract username and password for encryption
            username = db_data.pop('username', None)
            password = db_data.pop('password', None)

            # Use hostname and schema as unique identifier
            database, created = Database.objects.get_or_create(
                hostname=db_data['hostname'],
                schema=db_data['schema'],
                defaults=db_data
            )

            if created:
                # Set encrypted credentials
                if username:
                    database.set_encrypted_username(username)
                if password:
                    database.set_encrypted_password(password)
                database.save()

                self.stdout.write(f'  Created: {database.hostname}/{database.schema}')
            else:
                self.stdout.write(f'  Already exists: {database.hostname}/{database.schema}')
