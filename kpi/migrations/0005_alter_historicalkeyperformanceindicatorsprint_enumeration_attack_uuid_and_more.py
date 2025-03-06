# Generated by Django 5.1.6 on 2025-03-06 01:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0004_fix_enumeration_attack_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalkeyperformanceindicatorsprint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='keyperformanceindicatorsprint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
