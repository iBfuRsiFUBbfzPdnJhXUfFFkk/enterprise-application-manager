from django.core.management.base import BaseCommand
from core.views.database_size.database_size_view import record_snapshot


class Command(BaseCommand):
    help = 'Records a snapshot of current database table sizes for trend analysis'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Recording database size snapshot...'))

        try:
            count = record_snapshot()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully recorded snapshot with {count} table records'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error recording snapshot: {str(e)}')
            )
            raise
