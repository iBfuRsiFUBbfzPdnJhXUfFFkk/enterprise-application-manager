import hashlib

from django.core.management.base import BaseCommand
from django.db.models import Count

from core.models.document import Document


class Command(BaseCommand):
    help = 'Calculate SHA-256 hashes for existing documents without hashes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Recalculate hashes for all documents, not just those missing hashes',
        )

    def handle(self, *args, **options):
        if options['all']:
            documents = Document.objects.filter(file__isnull=False).exclude(file='')
        else:
            documents = Document.objects.filter(
                file__isnull=False,
                file_hash__isnull=True
            ).exclude(file='')

        total = documents.count()
        self.stdout.write(f"Found {total} document(s) to process")

        updated = 0
        errors = 0

        for doc in documents:
            try:
                if doc.file:
                    doc.file.seek(0)
                    sha256 = hashlib.sha256()
                    for chunk in doc.file.chunks():
                        sha256.update(chunk)
                    doc.file_hash = sha256.hexdigest()
                    doc.save(update_fields=['file_hash'])
                    updated += 1
                    self.stdout.write(f"  Hashed: {doc.name} -> {doc.file_hash[:16]}...")
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f"  Error hashing {doc.name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nCompleted: {updated} hashed, {errors} errors"))

        # Show duplicates summary
        duplicates = Document.objects.filter(
            file_hash__isnull=False
        ).values('file_hash').annotate(
            count=Count('id')
        ).filter(count__gt=1)

        if duplicates:
            self.stdout.write(self.style.WARNING(f"\nFound {len(duplicates)} duplicate file(s):"))
            for dup in duplicates:
                docs = Document.objects.filter(file_hash=dup['file_hash'])
                self.stdout.write(f"  Hash {dup['file_hash'][:16]}... ({dup['count']} copies):")
                for d in docs:
                    self.stdout.write(f"    - {d.name} (ID: {d.id})")
