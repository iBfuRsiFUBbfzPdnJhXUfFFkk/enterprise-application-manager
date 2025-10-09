from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.person import Person
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool
from core.models.common.enums.authentication_choices import AUTHENTICATION_TYPE_AD, AUTHENTICATION_TYPE_CUSTOM
from core.models.common.enums.authorization_choices import AUTHORIZATION_TYPE_AD, AUTHORIZATION_TYPE_CUSTOM
from core.models.common.enums.deployment_medium_choices import (
    DEPLOYMENT_MEDIUM_CLOUD_DIVIO,
    DEPLOYMENT_MEDIUM_CLOUD_AKS,
    DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX
)
from core.models.common.enums.lifecycle_choices import (
    LIFECYCLE_ACTIVE,
    LIFECYCLE_DEVELOPMENT,
    LIFECYCLE_PLANNING,
    LIFECYCLE_DEPRECATED
)
from core.models.common.enums.platform_target_choices import (
    PLATFORM_TARGET_WEB,
    PLATFORM_TARGET_IOS,
    PLATFORM_TARGET_BACKGROUND_TASK
)


class Command(BaseCommand):
    help = 'Populates the database with test data for applications and related models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        with transaction.atomic():
            # Create People
            self.stdout.write('Creating people...')
            people = self.create_people()

            # Create Application Groups
            self.stdout.write('Creating application groups...')
            app_groups = self.create_application_groups()

            # Create Service Providers
            self.stdout.write('Creating service providers...')
            service_providers = self.create_service_providers()

            # Create Tools
            self.stdout.write('Creating tools...')
            tools = self.create_tools()

            # Create Applications
            self.stdout.write('Creating applications...')
            self.create_applications(people, app_groups, service_providers, tools)

        self.stdout.write(self.style.SUCCESS('Database population complete!'))

    def create_people(self):
        """Create test people with various roles"""
        people_data = [
            {
                'name_first': 'John',
                'name_last': 'Smith',
                'communication_email': 'john.smith@example.com',
                'is_product_owner': True,
                'is_active': True,
            },
            {
                'name_first': 'Sarah',
                'name_last': 'Johnson',
                'communication_email': 'sarah.johnson@example.com',
                'is_product_manager': True,
                'is_active': True,
            },
            {
                'name_first': 'Michael',
                'name_last': 'Williams',
                'communication_email': 'michael.williams@example.com',
                'is_project_manager': True,
                'is_active': True,
            },
            {
                'name_first': 'Emily',
                'name_last': 'Brown',
                'communication_email': 'emily.brown@example.com',
                'is_scrum_master': True,
                'is_active': True,
            },
            {
                'name_first': 'David',
                'name_last': 'Davis',
                'communication_email': 'david.davis@example.com',
                'is_architect': True,
                'is_active': True,
            },
            {
                'name_first': 'Jennifer',
                'name_last': 'Martinez',
                'communication_email': 'jennifer.martinez@example.com',
                'is_lead_developer': True,
                'is_active': True,
            },
            {
                'name_first': 'Robert',
                'name_last': 'Garcia',
                'communication_email': 'robert.garcia@example.com',
                'is_developer': True,
                'is_active': True,
            },
            {
                'name_first': 'Lisa',
                'name_last': 'Rodriguez',
                'communication_email': 'lisa.rodriguez@example.com',
                'is_developer': True,
                'is_active': True,
            },
            {
                'name_first': 'James',
                'name_last': 'Wilson',
                'communication_email': 'james.wilson@example.com',
                'is_stakeholder': True,
                'is_active': True,
            },
        ]

        people = {}
        for person_data in people_data:
            person, created = Person.objects.get_or_create(
                name_first=person_data['name_first'],
                name_last=person_data['name_last'],
                defaults=person_data
            )
            key = person_data['name_first'].lower()
            people[key] = person
            if created:
                self.stdout.write(f'  Created: {person.full_name_for_human}')
            else:
                self.stdout.write(f'  Already exists: {person.full_name_for_human}')

        return people

    def create_application_groups(self):
        """Create test application groups"""
        groups_data = [
            {
                'name': 'Enterprise Platform',
                'acronym': 'EP',
                'aliases_csv': 'Platform',
                'comment': 'Core enterprise platform applications',
                'is_platform': True,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Customer Facing',
                'acronym': 'CF',
                'aliases_csv': 'Customer',
                'comment': 'Applications that directly serve customers',
                'is_externally_facing': True,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Internal Tools',
                'acronym': 'IT',
                'aliases_csv': 'Tools',
                'comment': 'Internal productivity and management tools',
                'is_platform': False,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
        ]

        groups = {}
        for group_data in groups_data:
            group, created = ApplicationGroup.objects.get_or_create(
                name=group_data['name'],
                defaults=group_data
            )
            groups[group_data['acronym'].lower()] = group
            if created:
                self.stdout.write(f'  Created: {group.name}')
            else:
                self.stdout.write(f'  Already exists: {group.name}')

        return groups

    def create_service_providers(self):
        """Create test service providers"""
        providers_data = [
            {
                'name': 'Amazon Web Services',
                'comment': 'Cloud infrastructure provider',
                'url': 'https://aws.amazon.com',
            },
            {
                'name': 'Microsoft Azure',
                'comment': 'Cloud platform and services',
                'url': 'https://azure.microsoft.com',
            },
            {
                'name': 'SendGrid',
                'comment': 'Email delivery service',
                'url': 'https://sendgrid.com',
            },
            {
                'name': 'Stripe',
                'comment': 'Payment processing platform',
                'url': 'https://stripe.com',
            },
        ]

        providers = {}
        for provider_data in providers_data:
            provider, created = ServiceProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults=provider_data
            )
            providers[provider_data['name'].lower().replace(' ', '_')] = provider
            if created:
                self.stdout.write(f'  Created: {provider.name}')
            else:
                self.stdout.write(f'  Already exists: {provider.name}')

        return providers

    def create_tools(self):
        """Create test tools"""
        tools_data = [
            {
                'name': 'Django',
                'comment': 'Python web framework',
                'url': 'https://www.djangoproject.com',
            },
            {
                'name': 'React',
                'comment': 'JavaScript UI library',
                'url': 'https://react.dev',
            },
            {
                'name': 'PostgreSQL',
                'comment': 'Relational database',
                'url': 'https://www.postgresql.org',
            },
            {
                'name': 'Redis',
                'comment': 'In-memory data store',
                'url': 'https://redis.io',
            },
            {
                'name': 'Docker',
                'comment': 'Container platform',
                'url': 'https://www.docker.com',
            },
        ]

        tools = {}
        for tool_data in tools_data:
            tool, created = Tool.objects.get_or_create(
                name=tool_data['name'],
                defaults=tool_data
            )
            tools[tool_data['name'].lower()] = tool
            if created:
                self.stdout.write(f'  Created: {tool.name}')
            else:
                self.stdout.write(f'  Already exists: {tool.name}')

        return tools

    def create_applications(self, people, app_groups, service_providers, tools):
        """Create test applications"""
        applications_data = [
            {
                'name': 'Customer Portal',
                'acronym': 'CP',
                'aliases_csv': 'Portal',
                'comment': 'Self-service customer portal for account management',
                'type_platform_target': PLATFORM_TARGET_WEB,
                'type_deployment_medium': DEPLOYMENT_MEDIUM_CLOUD_DIVIO,
                'type_authentication': AUTHENTICATION_TYPE_AD,
                'type_authorization': AUTHORIZATION_TYPE_AD,
                'type_lifecycle': LIFECYCLE_ACTIVE,
                'platform_group': app_groups.get('cf'),
                'groups': [app_groups.get('cf'), app_groups.get('ep')],
                'peak_userbase': 10000,
                'date_launch': date.today() - timedelta(days=365),
                'is_externally_facing': True,
                'is_legacy': False,
                'is_using_artificial_intelligence': True,
                'is_storing_personally_identifiable_information_pii': True,
                'is_required_to_adhere_to_general_data_protection_regulation_gdpr': True,
                'link_gitlab_repository': 'https://gitlab.example.com/customer-portal',
                'link_production_server': 'https://portal.example.com',
                'link_sentry_io': 'https://sentry.io/customer-portal',
                'product_owner': people.get('john'),
                'product_manager': people.get('sarah'),
                'architect': people.get('david'),
                'lead_developer': people.get('jennifer'),
                'developers': [people.get('robert'), people.get('lisa')],
                'stakeholders': [people.get('james')],
                'service_providers': [service_providers.get('amazon_web_services'), service_providers.get('sendgrid')],
                'tools': [tools.get('django'), tools.get('react'), tools.get('postgresql')],
            },
            {
                'name': 'Enterprise Resource Planning',
                'acronym': 'ERP',
                'aliases_csv': 'ERP System',
                'comment': 'Comprehensive ERP system for business operations',
                'type_platform_target': PLATFORM_TARGET_WEB,
                'type_deployment_medium': DEPLOYMENT_MEDIUM_CLOUD_AKS,
                'type_authentication': AUTHENTICATION_TYPE_AD,
                'type_authorization': AUTHORIZATION_TYPE_AD,
                'type_lifecycle': LIFECYCLE_ACTIVE,
                'platform_group': app_groups.get('ep'),
                'groups': [app_groups.get('ep'), app_groups.get('it')],
                'peak_userbase': 500,
                'date_launch': date.today() - timedelta(days=730),
                'is_externally_facing': False,
                'is_legacy': False,
                'is_storing_personally_identifiable_information_pii': True,
                'is_storing_protected_health_information_phi': False,
                'link_gitlab_repository': 'https://gitlab.example.com/erp',
                'link_production_server': 'https://erp.internal.example.com',
                'product_owner': people.get('john'),
                'scrum_master': people.get('emily'),
                'architect': people.get('david'),
                'lead_developer': people.get('jennifer'),
                'developers': [people.get('robert'), people.get('lisa')],
                'service_providers': [service_providers.get('microsoft_azure')],
                'tools': [tools.get('django'), tools.get('postgresql'), tools.get('redis')],
            },
            {
                'name': 'Mobile Banking App',
                'acronym': 'MBA',
                'aliases_csv': 'Mobile Banking',
                'comment': 'iOS mobile application for banking services',
                'type_platform_target': PLATFORM_TARGET_IOS,
                'type_deployment_medium': DEPLOYMENT_MEDIUM_CLOUD_DIVIO,
                'type_authentication': AUTHENTICATION_TYPE_CUSTOM,
                'type_authorization': AUTHORIZATION_TYPE_CUSTOM,
                'type_lifecycle': LIFECYCLE_DEVELOPMENT,
                'platform_group': app_groups.get('cf'),
                'groups': [app_groups.get('cf')],
                'peak_userbase': 50000,
                'date_launch': date.today() + timedelta(days=90),
                'is_externally_facing': True,
                'is_legacy': False,
                'is_storing_personally_identifiable_information_pii': True,
                'is_storing_nonpublic_personal_information_npi': True,
                'is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss': True,
                'link_gitlab_repository': 'https://gitlab.example.com/mobile-banking',
                'product_manager': people.get('sarah'),
                'project_manager': people.get('michael'),
                'architect': people.get('david'),
                'developers': [people.get('robert'), people.get('lisa')],
                'stakeholders': [people.get('james')],
                'service_providers': [service_providers.get('stripe'), service_providers.get('amazon_web_services')],
                'tools': [tools.get('react'), tools.get('postgresql')],
            },
            {
                'name': 'Data Sync Service',
                'acronym': 'DSS',
                'aliases_csv': 'Sync Service',
                'comment': 'Background task for synchronizing data across systems',
                'type_platform_target': PLATFORM_TARGET_BACKGROUND_TASK,
                'type_deployment_medium': DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX,
                'type_authentication': AUTHENTICATION_TYPE_CUSTOM,
                'type_authorization': AUTHORIZATION_TYPE_CUSTOM,
                'type_lifecycle': LIFECYCLE_ACTIVE,
                'platform_group': app_groups.get('ep'),
                'groups': [app_groups.get('ep'), app_groups.get('it')],
                'peak_userbase': 0,
                'date_launch': date.today() - timedelta(days=180),
                'is_externally_facing': False,
                'is_legacy': False,
                'link_gitlab_repository': 'https://gitlab.example.com/data-sync',
                'link_production_server': 'https://sync.internal.example.com',
                'architect': people.get('david'),
                'lead_developer': people.get('jennifer'),
                'developers': [people.get('robert')],
                'tools': [tools.get('django'), tools.get('postgresql'), tools.get('docker')],
            },
            {
                'name': 'Legacy Reporting System',
                'acronym': 'LRS',
                'aliases_csv': 'Old Reports',
                'comment': 'Legacy reporting system scheduled for deprecation',
                'type_platform_target': PLATFORM_TARGET_WEB,
                'type_deployment_medium': DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX,
                'type_authentication': AUTHENTICATION_TYPE_AD,
                'type_authorization': AUTHORIZATION_TYPE_AD,
                'type_lifecycle': LIFECYCLE_DEPRECATED,
                'platform_group': app_groups.get('it'),
                'groups': [app_groups.get('it')],
                'peak_userbase': 50,
                'date_launch': date.today() - timedelta(days=1825),
                'is_externally_facing': False,
                'is_legacy': True,
                'link_production_server': 'https://reports-old.internal.example.com',
                'developers': [people.get('robert')],
                'tools': [tools.get('postgresql')],
            },
        ]

        for app_data in applications_data:
            app, created = Application.objects.get_or_create(
                name=app_data['name'],
                defaults={
                    'acronym': app_data['acronym'],
                    'aliases_csv': app_data['aliases_csv'],
                    'comment': app_data['comment'],
                    'type_platform_target': app_data['type_platform_target'],
                    'type_deployment_medium': app_data['type_deployment_medium'],
                    'type_authentication': app_data['type_authentication'],
                    'type_authorization': app_data['type_authorization'],
                    'type_lifecycle': app_data['type_lifecycle'],
                    'application_group_platform': app_data['platform_group'],
                    'peak_userbase': app_data['peak_userbase'],
                    'date_launch': app_data['date_launch'],
                    'is_externally_facing': app_data.get('is_externally_facing', False),
                    'is_legacy': app_data.get('is_legacy', False),
                    'is_using_artificial_intelligence': app_data.get('is_using_artificial_intelligence', False),
                    'is_storing_personally_identifiable_information_pii': app_data.get('is_storing_personally_identifiable_information_pii', False),
                    'is_storing_protected_health_information_phi': app_data.get('is_storing_protected_health_information_phi', False),
                    'is_storing_nonpublic_personal_information_npi': app_data.get('is_storing_nonpublic_personal_information_npi', False),
                    'is_required_to_adhere_to_general_data_protection_regulation_gdpr': app_data.get('is_required_to_adhere_to_general_data_protection_regulation_gdpr', False),
                    'is_required_to_adhere_to_california_consumer_privacy_act_ccpa': app_data.get('is_required_to_adhere_to_california_consumer_privacy_act_ccpa', False),
                    'is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss': app_data.get('is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss', False),
                    'link_gitlab_repository': app_data.get('link_gitlab_repository', ''),
                    'link_production_server': app_data.get('link_production_server', ''),
                    'link_sentry_io': app_data.get('link_sentry_io', ''),
                    'person_product_owner': app_data.get('product_owner'),
                    'person_product_manager': app_data.get('product_manager'),
                    'person_project_manager': app_data.get('project_manager'),
                    'person_scrum_master': app_data.get('scrum_master'),
                    'person_architect': app_data.get('architect'),
                    'person_lead_developer': app_data.get('lead_developer'),
                }
            )

            if created:
                # Add many-to-many relationships
                if 'groups' in app_data:
                    app.application_groups.set(app_data['groups'])
                if 'developers' in app_data:
                    app.person_developers.set(app_data['developers'])
                if 'stakeholders' in app_data:
                    app.person_stakeholders.set(app_data['stakeholders'])
                if 'service_providers' in app_data:
                    app.service_providers.set(app_data['service_providers'])
                if 'tools' in app_data:
                    app.tools.set(app_data['tools'])

                self.stdout.write(f'  Created: {app.name}')
            else:
                self.stdout.write(f'  Already exists: {app.name}')
