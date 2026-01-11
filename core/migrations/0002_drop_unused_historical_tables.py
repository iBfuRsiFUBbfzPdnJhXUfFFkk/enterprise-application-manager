# Generated manually to drop Historical tables for models with _disable_history = True

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "DROP TABLE IF EXISTS core_historicalapplicationpin;",
                "DROP TABLE IF EXISTS core_historicaluserbookmark;",
            ],
            reverse_sql=[
                # Dropping tables is irreversible - raise an error if attempting to reverse
                "SELECT 'Cannot recreate dropped historical tables. Restore from backup if needed.';"
            ],
        ),
    ]
