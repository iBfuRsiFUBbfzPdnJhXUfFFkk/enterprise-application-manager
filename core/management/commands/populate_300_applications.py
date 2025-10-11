import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.person import Person
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool
from core.models.common.enums.authentication_choices import (
    AUTHENTICATION_TYPE_AD,
    AUTHENTICATION_TYPE_CUSTOM
)
from core.models.common.enums.authorization_choices import (
    AUTHORIZATION_TYPE_AD,
    AUTHORIZATION_TYPE_CUSTOM
)
from core.models.common.enums.deployment_medium_choices import (
    DEPLOYMENT_MEDIUM_CLOUD_DIVIO,
    DEPLOYMENT_MEDIUM_CLOUD_AKS,
    DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX,
    DEPLOYMENT_MEDIUM_ON_PREMISES_IIS
)
from core.models.common.enums.lifecycle_choices import (
    LIFECYCLE_ACTIVE,
    LIFECYCLE_APPROVAL,
    LIFECYCLE_DEPRECATED,
    LIFECYCLE_DEVELOPMENT,
    LIFECYCLE_HYPER_CARE,
    LIFECYCLE_IDEA,
    LIFECYCLE_IN_DEPRECATION,
    LIFECYCLE_LIMITED_SUPPORT,
    LIFECYCLE_PLANNING,
    LIFECYCLE_REJECTED
)
from core.models.common.enums.platform_target_choices import (
    PLATFORM_TARGET_WEB,
    PLATFORM_TARGET_IOS,
    PLATFORM_TARGET_BACKGROUND_TASK,
    PLATFORM_TARGET_CHROME_PLUGIN,
    PLATFORM_TARGET_MICROSOFT_EXCEL,
    PLATFORM_TARGET_MICROSOFT_EXCEL_VBA,
    PLATFORM_TARGET_MICROSOFT_WORD
)


class Command(BaseCommand):
    help = 'Populates the database with 300 test applications and application groups with all fields filled'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting generation of 300 applications...'))

        with transaction.atomic():
            # First, create prerequisite data
            self.stdout.write('Creating prerequisite data...')
            people = self.ensure_people()
            app_groups = self.ensure_application_groups()
            service_providers = self.ensure_service_providers()
            tools = self.ensure_tools()

            # Create 300 applications
            self.stdout.write('Creating 300 applications...')
            self.create_applications(people, app_groups, service_providers, tools)

        self.stdout.write(self.style.SUCCESS('Successfully created 300 applications!'))

    def ensure_people(self):
        """Ensure we have enough people for testing"""
        first_names = [
            'John', 'Sarah', 'Michael', 'Emily', 'David', 'Jennifer', 'Robert', 'Lisa',
            'James', 'Mary', 'William', 'Patricia', 'Richard', 'Linda', 'Thomas', 'Barbara',
            'Charles', 'Elizabeth', 'Daniel', 'Susan', 'Matthew', 'Jessica', 'Anthony', 'Karen',
            'Mark', 'Nancy', 'Donald', 'Betty', 'Steven', 'Helen'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Martinez', 'Garcia', 'Rodriguez',
            'Wilson', 'Anderson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Lee',
            'Thompson', 'White', 'Harris', 'Clark', 'Lewis', 'Walker', 'Hall', 'Allen',
            'Young', 'King', 'Wright', 'Lopez', 'Hill', 'Scott'
        ]

        people = []
        existing_count = Person.objects.count()

        if existing_count >= 30:
            people = list(Person.objects.all()[:30])
            self.stdout.write(f'  Using existing {len(people)} people')
        else:
            # Create people if needed
            for i in range(30 - existing_count):
                person, created = Person.objects.get_or_create(
                    name_first=first_names[i % len(first_names)],
                    name_last=last_names[i % len(last_names)],
                    defaults={
                        'communication_email': f'{first_names[i % len(first_names)].lower()}.{last_names[i % len(last_names)].lower()}@example.com',
                        'is_active': True,
                        'is_developer': i % 3 == 0,
                        'is_lead_developer': i % 10 == 0,
                        'is_architect': i % 15 == 0,
                        'is_product_owner': i % 20 == 0,
                        'is_product_manager': i % 12 == 0,
                        'is_project_manager': i % 14 == 0,
                        'is_scrum_master': i % 18 == 0,
                        'is_stakeholder': i % 5 == 0,
                    }
                )
                people.append(person)
                if created:
                    self.stdout.write(f'  Created: {person.full_name_for_human}')

            # Add any existing people
            people.extend(list(Person.objects.all()[:30]))

        return people

    def ensure_application_groups(self):
        """Ensure we have application groups"""
        groups_data = [
            {
                'name': 'Enterprise Platform',
                'acronym': 'EP',
                'aliases_csv': 'Platform,Core Platform',
                'comment': '## Enterprise Platform\n\nCore enterprise platform applications that provide foundational services.\n\n- Infrastructure services\n- Authentication and authorization\n- Data management',
                'is_platform': True,
                'is_externally_facing': False,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Customer Facing',
                'acronym': 'CF',
                'aliases_csv': 'Customer,Public,External',
                'comment': '## Customer Facing Applications\n\nApplications that directly serve customers and external users.\n\n- Public websites\n- Customer portals\n- Mobile applications',
                'is_platform': False,
                'is_externally_facing': True,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Internal Tools',
                'acronym': 'IT',
                'aliases_csv': 'Tools,Internal',
                'comment': '## Internal Tools\n\nInternal productivity and management tools for staff.\n\n- Admin dashboards\n- Reporting tools\n- Management applications',
                'is_platform': False,
                'is_externally_facing': False,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Data Analytics',
                'acronym': 'DA',
                'aliases_csv': 'Analytics,BI,Business Intelligence',
                'comment': '## Data Analytics\n\nBusiness intelligence and data analytics applications.\n\n- Reporting engines\n- Data visualization\n- Analytics platforms',
                'is_platform': False,
                'is_externally_facing': False,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Integration Services',
                'acronym': 'IS',
                'aliases_csv': 'Integration,API,Services',
                'comment': '## Integration Services\n\nAPI and integration services connecting systems.\n\n- REST APIs\n- Webhooks\n- Event processing',
                'is_platform': True,
                'is_externally_facing': True,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
            {
                'name': 'Legacy Systems',
                'acronym': 'LS',
                'aliases_csv': 'Legacy,Old Systems,Deprecated',
                'comment': '## Legacy Systems\n\nOlder systems being phased out or maintained.\n\n- Migration targets\n- Maintenance mode\n- Limited support',
                'is_platform': False,
                'is_externally_facing': False,
                'type_lifecycle': LIFECYCLE_LIMITED_SUPPORT,
            },
            {
                'name': 'Experimental',
                'acronym': 'EX',
                'aliases_csv': 'Experimental,Proof of Concept,POC',
                'comment': '## Experimental\n\nExperimental applications and proofs of concept.\n\n- Prototypes\n- Research projects\n- Innovation lab',
                'is_platform': False,
                'is_externally_facing': False,
                'type_lifecycle': LIFECYCLE_DEVELOPMENT,
            },
            {
                'name': 'Mobile Applications',
                'acronym': 'MA',
                'aliases_csv': 'Mobile,Apps',
                'comment': '## Mobile Applications\n\nMobile-first applications and services.\n\n- iOS apps\n- Android apps\n- Progressive web apps',
                'is_platform': False,
                'is_externally_facing': True,
                'type_lifecycle': LIFECYCLE_ACTIVE,
            },
        ]

        groups = []
        for group_data in groups_data:
            group, created = ApplicationGroup.objects.get_or_create(
                name=group_data['name'],
                defaults=group_data
            )
            groups.append(group)
            if created:
                self.stdout.write(f'  Created: {group.name}')

        return groups

    def ensure_service_providers(self):
        """Ensure we have service providers"""
        providers_data = [
            {'name': 'Amazon Web Services', 'comment': 'AWS cloud infrastructure provider', 'url': 'https://aws.amazon.com'},
            {'name': 'Microsoft Azure', 'comment': 'Azure cloud platform and services', 'url': 'https://azure.microsoft.com'},
            {'name': 'Google Cloud Platform', 'comment': 'GCP cloud computing services', 'url': 'https://cloud.google.com'},
            {'name': 'SendGrid', 'comment': 'Email delivery service', 'url': 'https://sendgrid.com'},
            {'name': 'Twilio', 'comment': 'Communications platform', 'url': 'https://www.twilio.com'},
            {'name': 'Stripe', 'comment': 'Payment processing platform', 'url': 'https://stripe.com'},
            {'name': 'Auth0', 'comment': 'Authentication and authorization platform', 'url': 'https://auth0.com'},
            {'name': 'Cloudflare', 'comment': 'CDN and security services', 'url': 'https://www.cloudflare.com'},
            {'name': 'Datadog', 'comment': 'Monitoring and analytics', 'url': 'https://www.datadoghq.com'},
            {'name': 'Sentry', 'comment': 'Error tracking and monitoring', 'url': 'https://sentry.io'},
        ]

        providers = []
        for provider_data in providers_data:
            provider, created = ServiceProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults=provider_data
            )
            providers.append(provider)
            if created:
                self.stdout.write(f'  Created: {provider.name}')

        return providers

    def ensure_tools(self):
        """Ensure we have tools"""
        tools_data = [
            {'name': 'Django', 'comment': 'Python web framework', 'url': 'https://www.djangoproject.com'},
            {'name': 'React', 'comment': 'JavaScript UI library', 'url': 'https://react.dev'},
            {'name': 'Vue.js', 'comment': 'Progressive JavaScript framework', 'url': 'https://vuejs.org'},
            {'name': 'Angular', 'comment': 'TypeScript web framework', 'url': 'https://angular.io'},
            {'name': 'PostgreSQL', 'comment': 'Relational database', 'url': 'https://www.postgresql.org'},
            {'name': 'MySQL', 'comment': 'Relational database', 'url': 'https://www.mysql.com'},
            {'name': 'MongoDB', 'comment': 'NoSQL document database', 'url': 'https://www.mongodb.com'},
            {'name': 'Redis', 'comment': 'In-memory data store', 'url': 'https://redis.io'},
            {'name': 'Docker', 'comment': 'Container platform', 'url': 'https://www.docker.com'},
            {'name': 'Kubernetes', 'comment': 'Container orchestration', 'url': 'https://kubernetes.io'},
            {'name': 'GitLab', 'comment': 'DevOps platform', 'url': 'https://gitlab.com'},
            {'name': 'Jenkins', 'comment': 'Automation server', 'url': 'https://www.jenkins.io'},
            {'name': 'Terraform', 'comment': 'Infrastructure as code', 'url': 'https://www.terraform.io'},
            {'name': 'Ansible', 'comment': 'Configuration management', 'url': 'https://www.ansible.com'},
        ]

        tools = []
        for tool_data in tools_data:
            tool, created = Tool.objects.get_or_create(
                name=tool_data['name'],
                defaults=tool_data
            )
            tools.append(tool)
            if created:
                self.stdout.write(f'  Created: {tool.name}')

        return tools

    def create_applications(self, people, app_groups, service_providers, tools):
        """Create 300 test applications with all fields populated"""

        # Application name components
        adjectives = [
            'Advanced', 'Smart', 'Digital', 'Cloud', 'Enterprise', 'Integrated', 'Intelligent',
            'Automated', 'Unified', 'Dynamic', 'Secure', 'Modern', 'Agile', 'Robust',
            'Scalable', 'Global', 'Real-time', 'Next-Gen', 'Strategic', 'Core'
        ]

        nouns = [
            'Portal', 'Platform', 'System', 'Service', 'Hub', 'Manager', 'Dashboard',
            'Gateway', 'Engine', 'Suite', 'Workspace', 'Console', 'Interface', 'Tool',
            'Solution', 'Framework', 'Network', 'Center', 'Application', 'API'
        ]

        domains = [
            'Customer', 'Employee', 'Partner', 'Vendor', 'Data', 'Analytics', 'Reporting',
            'Finance', 'HR', 'Marketing', 'Sales', 'Operations', 'Supply Chain', 'Inventory',
            'Project', 'Resource', 'Asset', 'Document', 'Content', 'Communication',
            'Collaboration', 'Workflow', 'Business', 'Product', 'Quality', 'Compliance',
            'Security', 'Identity', 'Access', 'Payment'
        ]

        auth_types = [AUTHENTICATION_TYPE_AD, AUTHENTICATION_TYPE_CUSTOM]
        authz_types = [AUTHORIZATION_TYPE_AD, AUTHORIZATION_TYPE_CUSTOM]
        deployment_types = [
            DEPLOYMENT_MEDIUM_CLOUD_DIVIO,
            DEPLOYMENT_MEDIUM_CLOUD_AKS,
            DEPLOYMENT_MEDIUM_ON_PREMISES_LINUX,
            DEPLOYMENT_MEDIUM_ON_PREMISES_IIS
        ]
        lifecycle_types = [
            LIFECYCLE_ACTIVE, LIFECYCLE_DEVELOPMENT, LIFECYCLE_PLANNING,
            LIFECYCLE_HYPER_CARE, LIFECYCLE_LIMITED_SUPPORT, LIFECYCLE_DEPRECATED,
            LIFECYCLE_IDEA, LIFECYCLE_APPROVAL, LIFECYCLE_IN_DEPRECATION
        ]
        platform_types = [
            PLATFORM_TARGET_WEB, PLATFORM_TARGET_IOS, PLATFORM_TARGET_BACKGROUND_TASK,
            PLATFORM_TARGET_CHROME_PLUGIN, PLATFORM_TARGET_MICROSOFT_EXCEL,
            PLATFORM_TARGET_MICROSOFT_EXCEL_VBA, PLATFORM_TARGET_MICROSOFT_WORD
        ]

        created_count = 0

        for i in range(1, 301):
            # Generate unique name
            domain = random.choice(domains)
            adjective = random.choice(adjectives)
            noun = random.choice(nouns)
            name = f"{domain} {adjective} {noun} {i}"

            # Generate acronym from first letters
            acronym = ''.join([word[0] for word in name.split()[:3]]).upper()

            # Generate aliases
            aliases = [
                f"{domain} {noun}",
                f"{adjective} {noun}",
                f"{domain} System"
            ]

            # Generate dates
            days_ago = random.randint(-180, 1825)  # Some future, most past
            launch_date = date.today() - timedelta(days=days_ago)

            # Random selections
            is_legacy = random.random() < 0.15  # 15% legacy
            is_externally_facing = random.random() < 0.40  # 40% external
            is_ai = random.random() < 0.25  # 25% use AI

            # Privacy/compliance flags
            has_pii = random.random() < 0.60  # 60% have PII
            has_phi = random.random() < 0.10  # 10% have PHI
            has_npi = random.random() < 0.20  # 20% have NPI
            needs_gdpr = is_externally_facing and random.random() < 0.50
            needs_ccpa = is_externally_facing and random.random() < 0.40
            needs_pci = random.random() < 0.15  # 15% need PCI-DSS

            # Generate comment with markdown
            comment = f"""## {name}

### Overview
{name} is a {'legacy' if is_legacy else 'modern'} {'externally-facing' if is_externally_facing else 'internal'} application that provides {domain.lower()} services.

### Key Features
- **Peak Users**: {random.randint(10, 100000):,} users
- **Authentication**: {random.choice(auth_types)}
- **Deployment**: {random.choice(deployment_types)}
- **AI-Powered**: {'Yes' if is_ai else 'No'}

### Compliance
{'- **GDPR Compliant**' if needs_gdpr else ''}
{'- **CCPA Compliant**' if needs_ccpa else ''}
{'- **PCI-DSS Certified**' if needs_pci else ''}

### Data Handling
{'- Stores PII' if has_pii else ''}
{'- Stores PHI' if has_phi else ''}
{'- Stores NPI' if has_npi else ''}
"""

            # Create application
            app, created = Application.objects.get_or_create(
                name=name,
                defaults={
                    'acronym': acronym,
                    'aliases_csv': ','.join(aliases),
                    'comment': comment,

                    # Type fields
                    'type_authentication': random.choice(auth_types),
                    'type_authorization': random.choice(authz_types),
                    'type_deployment_medium': random.choice(deployment_types),
                    'type_lifecycle': random.choice(lifecycle_types),
                    'type_platform_target': random.choice(platform_types),

                    # Boolean fields
                    'is_externally_facing': is_externally_facing,
                    'is_legacy': is_legacy,
                    'is_using_artificial_intelligence': is_ai,
                    'is_storing_personally_identifiable_information_pii': has_pii,
                    'is_storing_protected_health_information_phi': has_phi,
                    'is_storing_nonpublic_personal_information_npi': has_npi,
                    'is_required_to_adhere_to_general_data_protection_regulation_gdpr': needs_gdpr,
                    'is_required_to_adhere_to_california_consumer_privacy_act_ccpa': needs_ccpa,
                    'is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss': needs_pci,

                    # Date fields
                    'date_launch': launch_date,

                    # Integer fields
                    'peak_userbase': random.randint(10, 100000),

                    # Link fields - populate ALL of them
                    'link_development_server': f'https://dev-app-{i}.example.com',
                    'link_divio': f'https://divio.com/app-{i}' if random.random() < 0.3 else '',
                    'link_gitlab_repository': f'https://gitlab.example.com/apps/{domain.lower()}-{noun.lower()}-{i}',
                    'link_gitlab_wiki': f'https://gitlab.example.com/apps/{domain.lower()}-{noun.lower()}-{i}/-/wikis/home',
                    'link_logs': f'https://logs.example.com/app-{i}',
                    'link_lucid': f'https://lucid.app/documents/app-{i}' if random.random() < 0.4 else '',
                    'link_open_ai': f'https://platform.openai.com/app-{i}' if is_ai else '',
                    'link_postman': f'https://www.postman.com/app-{i}/workspace' if random.random() < 0.5 else '',
                    'link_production_server': f'https://app-{i}.example.com',
                    'link_production_server_external': f'https://app-{i}.example.com/public' if is_externally_facing else '',
                    'link_sentry_io': f'https://sentry.io/organizations/example/projects/app-{i}',
                    'link_software_bill_of_materials_sbom': f'https://sbom.example.com/app-{i}',
                    'link_staging_server': f'https://staging-app-{i}.example.com',
                    'link_support_email': f'app-{i}-support@example.com',
                    'link_teams_channel': f'https://teams.microsoft.com/l/channel/app-{i}',
                    'link_training': f'https://training.example.com/app-{i}' if random.random() < 0.6 else '',
                    'link_ticket_submission': f'https://tickets.example.com/app-{i}',
                    'link_whiteboard': f'https://miro.com/app-{i}' if random.random() < 0.3 else '',
                    'link_wrike': f'https://www.wrike.com/workspace/app-{i}' if random.random() < 0.4 else '',

                    # Foreign keys
                    'application_group_platform': random.choice(app_groups),
                    'person_architect': random.choice(people) if random.random() < 0.8 else None,
                    'person_lead_developer': random.choice(people) if random.random() < 0.9 else None,
                    'person_product_manager': random.choice(people) if random.random() < 0.7 else None,
                    'person_product_owner': random.choice(people) if random.random() < 0.8 else None,
                    'person_project_manager': random.choice(people) if random.random() < 0.6 else None,
                    'person_scrum_master': random.choice(people) if random.random() < 0.7 else None,
                }
            )

            if created:
                # Many-to-many relationships
                app.application_groups.set(random.sample(app_groups, k=random.randint(1, 3)))
                app.person_developers.set(random.sample(people, k=random.randint(1, 5)))
                app.person_stakeholders.set(random.sample(people, k=random.randint(1, 4)))
                app.service_providers.set(random.sample(service_providers, k=random.randint(1, 4)))
                app.tools.set(random.sample(tools, k=random.randint(2, 6)))

                # Optionally set dependencies (for some apps)
                if i > 10 and random.random() < 0.3:  # 30% have dependencies
                    existing_apps = list(Application.objects.all()[:i-1])
                    if existing_apps:
                        app.application_upstream_dependencies.set(
                            random.sample(existing_apps, k=min(random.randint(1, 3), len(existing_apps)))
                        )

                created_count += 1
                if created_count % 25 == 0:
                    self.stdout.write(f'  Created {created_count} applications...')

        self.stdout.write(self.style.SUCCESS(f'  Total created: {created_count} applications'))
