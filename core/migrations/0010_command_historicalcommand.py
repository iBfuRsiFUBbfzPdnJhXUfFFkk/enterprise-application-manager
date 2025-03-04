# Generated by Django 5.1.6 on 2025-03-01 20:31

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_acronym_enumeration_attack_uuid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('command', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['name', '-id'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalCommand',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('command', models.CharField(blank=True, max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical command',
                'verbose_name_plural': 'historical commands',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
