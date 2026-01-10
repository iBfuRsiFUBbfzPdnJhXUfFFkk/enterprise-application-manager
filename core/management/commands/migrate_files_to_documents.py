"""
Management command to create Document records from existing file attachments.

This command:
1. Finds BadInteraction records with evidence_file but no linked documents
2. Finds BadInteractionUpdate records with attachment_file but no linked documents
3. Finds HRIncidentUpdate records with attachment_file but no linked documents
4. Creates Document records for each file
5. Links the new Document to the source record via M2M relationship

Usage:
    python manage.py migrate_files_to_documents [--dry-run]
"""

from django.core.management.base import BaseCommand
from core.models.bad_interaction import BadInteraction
from core.models.bad_interaction_update import BadInteractionUpdate
from core.models.document import Document
from core.models.hr_incident_update import HRIncidentUpdate


class Command(BaseCommand):
    help = 'Create Document records from existing file attachments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        stats = {
            'bad_interactions': 0,
            'bad_interaction_updates': 0,
            'hr_incident_updates': 0,
        }

        mode = 'DRY RUN' if dry_run else 'MIGRATION'
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 80}'))
        self.stdout.write(self.style.SUCCESS(f'Migrate Files to Documents - {mode} Mode'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 80}\n'))

        # Process BadInteractions
        self.stdout.write('Processing BadInteractions...')
        for bi in BadInteraction.objects.filter(evidence_file__isnull=False).exclude(evidence_file=''):
            # Skip if already has linked documents
            if bi.documents.exists():
                continue

            # Create Document name
            person_name = str(bi.person) if bi.person else 'Unknown'
            doc_name = f"BadInteraction Evidence - {person_name}"

            if not dry_run:
                # Create Document - reuse existing file path
                doc = Document.objects.create(
                    name=doc_name,
                    comment=f"Evidence file from BadInteraction #{bi.pk}",
                    file=bi.evidence_file.name,
                    migrated_to_minio=bi.migrated_to_minio,
                )
                bi.documents.add(doc)
                stats['bad_interactions'] += 1
                self.stdout.write(f"  Created: {doc_name}")
            else:
                self.stdout.write(f"  Would create: {doc_name}")
                stats['bad_interactions'] += 1

        # Process BadInteractionUpdates
        self.stdout.write('\nProcessing BadInteractionUpdates...')
        for update in BadInteractionUpdate.objects.filter(attachment_file__isnull=False).exclude(attachment_file=''):
            if update.documents.exists():
                continue

            person_name = str(update.bad_interaction.person) if update.bad_interaction.person else 'Unknown'
            doc_name = f"BadInteraction Update Attachment - {person_name}"

            if not dry_run:
                doc = Document.objects.create(
                    name=doc_name,
                    comment=f"Attachment from BadInteractionUpdate #{update.pk}",
                    file=update.attachment_file.name,
                    migrated_to_minio=update.migrated_to_minio,
                )
                update.documents.add(doc)
                stats['bad_interaction_updates'] += 1
                self.stdout.write(f"  Created: {doc_name}")
            else:
                self.stdout.write(f"  Would create: {doc_name}")
                stats['bad_interaction_updates'] += 1

        # Process HRIncidentUpdates
        self.stdout.write('\nProcessing HRIncidentUpdates...')
        for update in HRIncidentUpdate.objects.filter(attachment_file__isnull=False).exclude(attachment_file=''):
            if update.documents.exists():
                continue

            hr_incident = update.hr_incident
            incident_name = hr_incident.name if hr_incident else 'Unknown'
            doc_name = f"HR Incident Update Attachment - {incident_name}"

            if not dry_run:
                doc = Document.objects.create(
                    name=doc_name,
                    comment=f"Attachment from HRIncidentUpdate #{update.pk}",
                    file=update.attachment_file.name,
                    migrated_to_minio=update.migrated_to_minio,
                )
                update.documents.add(doc)
                stats['hr_incident_updates'] += 1
                self.stdout.write(f"  Created: {doc_name}")
            else:
                self.stdout.write(f"  Would create: {doc_name}")
                stats['hr_incident_updates'] += 1

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 80}'))
        self.stdout.write(self.style.SUCCESS('Summary'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 80}\n'))
        self.stdout.write(f"  BadInteractions: {stats['bad_interactions']} documents created")
        self.stdout.write(f"  BadInteractionUpdates: {stats['bad_interaction_updates']} documents created")
        self.stdout.write(f"  HRIncidentUpdates: {stats['hr_incident_updates']} documents created")
        total = sum(stats.values())
        self.stdout.write(f"\n  Total: {total} documents")

        if dry_run:
            self.stdout.write(self.style.WARNING('\nDry run - no changes made'))
        else:
            self.stdout.write(self.style.SUCCESS('\nMigration complete!'))
