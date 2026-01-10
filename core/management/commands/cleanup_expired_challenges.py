from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models.passkey_challenge import PasskeyChallenge


class Command(BaseCommand):
    help = 'Delete expired and used passkey challenges to keep database clean'

    def handle(self, *args, **options):
        now = timezone.now()
        cutoff_time = now - timedelta(hours=24)

        # Delete expired challenges
        expired_count, _ = PasskeyChallenge.objects.filter(expires_at__lt=now).delete()

        # Delete used challenges older than 24 hours
        old_used_count, _ = PasskeyChallenge.objects.filter(used=True, created_at__lt=cutoff_time).delete()

        total_deleted = expired_count + old_used_count

        if total_deleted > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {total_deleted} passkey challenge(s): '
                    f'{expired_count} expired, {old_used_count} old used'
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS('No expired passkey challenges to delete'))
