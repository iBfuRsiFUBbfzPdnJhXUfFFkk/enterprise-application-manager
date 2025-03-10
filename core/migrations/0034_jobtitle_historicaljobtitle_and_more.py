# Generated by Django 5.1.6 on 2025-03-07 20:43

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_historicaluser_options_alter_person_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(blank=True, max_length=255, null=True)),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Job Title',
                'verbose_name_plural': 'Job Titles',
                'ordering': ['name', '-id'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalJobTitle',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('acronym', models.CharField(blank=True, max_length=255, null=True)),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '_Historical Record for JobTitle',
                'verbose_name_plural': '_Historical Records for JobTitle',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='job_title',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.jobtitle'),
        ),
        migrations.AddField(
            model_name='person',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.jobtitle'),
        ),
    ]
