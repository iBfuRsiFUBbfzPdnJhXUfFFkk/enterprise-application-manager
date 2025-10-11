import random
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.application_group import ApplicationGroup
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


class Command(BaseCommand):
    help = 'Populates the database with 300 test application groups with all fields filled'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting generation of 300 application groups...'))

        with transaction.atomic():
            self.create_application_groups()

        self.stdout.write(self.style.SUCCESS('Successfully created 300 application groups!'))

    def create_application_groups(self):
        """Create 300 test application groups with all fields populated"""

        # Group name components
        adjectives = [
            'Advanced', 'Smart', 'Digital', 'Cloud', 'Enterprise', 'Integrated', 'Intelligent',
            'Automated', 'Unified', 'Dynamic', 'Secure', 'Modern', 'Agile', 'Robust',
            'Scalable', 'Global', 'Real-time', 'Next-Gen', 'Strategic', 'Core',
            'Premier', 'Elite', 'Professional', 'Essential', 'Premium', 'Ultimate',
            'Superior', 'Optimal', 'Enhanced', 'Revolutionary'
        ]

        domains = [
            'Customer', 'Employee', 'Partner', 'Vendor', 'Data', 'Analytics', 'Reporting',
            'Finance', 'HR', 'Marketing', 'Sales', 'Operations', 'Supply Chain', 'Inventory',
            'Project', 'Resource', 'Asset', 'Document', 'Content', 'Communication',
            'Collaboration', 'Workflow', 'Business', 'Product', 'Quality', 'Compliance',
            'Security', 'Identity', 'Access', 'Payment', 'Billing', 'Order', 'Shipping',
            'Manufacturing', 'Procurement', 'Contract', 'Legal', 'Audit', 'Risk',
            'Support', 'Service', 'Training', 'Learning', 'Knowledge', 'Innovation',
            'Research', 'Development', 'Testing', 'Deployment', 'Integration'
        ]

        group_types = [
            'Platform', 'Suite', 'Group', 'Division', 'Family', 'Collection', 'Portfolio',
            'Ecosystem', 'Framework', 'Stack', 'Cluster', 'Hub', 'Network', 'System',
            'Services', 'Solutions', 'Tools', 'Applications', 'Resources', 'Infrastructure'
        ]

        lifecycle_types = [
            LIFECYCLE_ACTIVE, LIFECYCLE_DEVELOPMENT, LIFECYCLE_PLANNING,
            LIFECYCLE_HYPER_CARE, LIFECYCLE_LIMITED_SUPPORT, LIFECYCLE_DEPRECATED,
            LIFECYCLE_IDEA, LIFECYCLE_APPROVAL, LIFECYCLE_IN_DEPRECATION, LIFECYCLE_REJECTED
        ]

        purposes = [
            'customer engagement', 'operational efficiency', 'data management',
            'business intelligence', 'workflow automation', 'collaboration',
            'financial management', 'human resources', 'security and compliance',
            'marketing automation', 'sales enablement', 'supply chain optimization',
            'project management', 'quality assurance', 'customer support',
            'content management', 'identity management', 'analytics and reporting',
            'integration services', 'API management', 'data warehousing',
            'business process management', 'document management', 'asset tracking',
            'inventory management', 'order processing', 'contract management',
            'compliance tracking', 'audit management', 'risk assessment',
            'training and development', 'knowledge management', 'innovation',
            'research and development', 'product lifecycle', 'testing and QA'
        ]

        benefits = [
            'improved efficiency', 'reduced costs', 'enhanced security',
            'better collaboration', 'faster time-to-market', 'improved quality',
            'better compliance', 'enhanced visibility', 'automated workflows',
            'streamlined processes', 'data-driven decisions', 'improved productivity',
            'better customer experience', 'reduced manual effort', 'scalable architecture',
            'improved reliability', 'faster deployment', 'better integration',
            'enhanced monitoring', 'improved governance'
        ]

        features = [
            'Real-time monitoring and alerts',
            'Advanced analytics and reporting',
            'API-first architecture',
            'Microservices-based design',
            'Cloud-native deployment',
            'Mobile-first interface',
            'Role-based access control',
            'Single sign-on integration',
            'Automated workflows',
            'Data encryption at rest and in transit',
            'Audit logging and compliance tracking',
            'Multi-tenant support',
            'Scalable infrastructure',
            'High availability and disaster recovery',
            'Automated testing and deployment',
            'Performance optimization',
            'Version control and rollback',
            'Customizable dashboards',
            'Integration with third-party services',
            'Machine learning capabilities'
        ]

        created_count = 0

        for i in range(1, 301):
            # Generate unique name
            domain = random.choice(domains)
            adjective = random.choice(adjectives)
            group_type = random.choice(group_types)
            name = f"{domain} {adjective} {group_type} {i}"

            # Generate acronym from first letters
            acronym = ''.join([word[0] for word in name.split()[:3]]).upper()

            # Generate aliases
            aliases = [
                f"{domain} {group_type}",
                f"{adjective} {group_type}",
                f"{domain} Suite",
                f"{domain} {adjective}"
            ]

            # Random selections
            is_platform = random.random() < 0.30  # 30% are platforms
            is_externally_facing = random.random() < 0.35  # 35% external

            # Select random purpose, benefits, and features
            selected_purpose = random.choice(purposes)
            selected_benefits = random.sample(benefits, k=random.randint(3, 6))
            selected_features = random.sample(features, k=random.randint(4, 8))

            # Generate comprehensive comment with markdown
            comment = f"""## {name}

### Overview
The {name} is a {'platform-level' if is_platform else 'application-level'} solution designed for {selected_purpose}. This {'externally-facing' if is_externally_facing else 'internal'} group provides comprehensive capabilities for {'external users and customers' if is_externally_facing else 'internal teams and stakeholders'}.

### Purpose
{name} serves as a strategic initiative to enhance organizational capabilities in the {domain.lower()} domain. It provides a unified approach to managing related applications and services.

### Key Benefits
"""
            for benefit in selected_benefits:
                comment += f"- **{benefit.title()}**\n"

            comment += f"""
### Features
"""
            for feature in selected_features:
                comment += f"- {feature}\n"

            comment += f"""
### Architecture
{'Platform services providing foundational capabilities' if is_platform else 'Application suite for specific business functions'}

### Target Audience
{'External customers, partners, and public users' if is_externally_facing else 'Internal employees, administrators, and business users'}

### Strategic Alignment
This group aligns with organizational goals for digital transformation, operational excellence, and {"customer experience improvement" if is_externally_facing else "internal process optimization"}.
"""

            # Create application group
            group, created = ApplicationGroup.objects.get_or_create(
                name=name,
                defaults={
                    'acronym': acronym,
                    'aliases_csv': ','.join(aliases),
                    'comment': comment,
                    'is_platform': is_platform,
                    'is_externally_facing': is_externally_facing,
                    'type_lifecycle': random.choice(lifecycle_types),
                }
            )

            if created:
                created_count += 1
                if created_count % 25 == 0:
                    self.stdout.write(f'  Created {created_count} application groups...')

        self.stdout.write(self.style.SUCCESS(f'  Total created: {created_count} application groups'))
