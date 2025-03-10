# Generated by Django 5.1.6 on 2025-03-04 18:30

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0015_remove_keyperformanceindicatorsprint_person_developer_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalKeyPerformanceIndicatorSprint',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('cached_capacity_adjusted', models.IntegerField(blank=True, null=True)),
                ('cached_capacity_per_day', models.DecimalField(blank=True, decimal_places=7, max_digits=20, null=True)),
                ('capacity_base', models.IntegerField(blank=True, null=True)),
                ('number_of_code_lines_added', models.IntegerField(blank=True, null=True)),
                ('number_of_code_lines_removed', models.IntegerField(blank=True, null=True)),
                ('number_of_code_reviews_submitted', models.IntegerField(blank=True, null=True)),
                ('number_of_comments_made', models.IntegerField(blank=True, null=True)),
                ('number_of_context_switches', models.IntegerField(blank=True, null=True)),
                ('number_of_issues_written', models.IntegerField(blank=True, null=True)),
                ('number_of_paid_time_off_days', models.IntegerField(blank=True, null=True)),
                ('number_of_story_points_committed_to', models.IntegerField(blank=True, null=True)),
                ('number_of_story_points_delivered', models.IntegerField(blank=True, null=True)),
                ('number_of_threads_resolved', models.IntegerField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('person_developer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.person')),
                ('sprint', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.sprint')),
            ],
            options={
                'verbose_name': 'historical key performance indicator sprint',
                'verbose_name_plural': 'historical key performance indicator sprints',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='KeyPerformanceIndicatorSprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('cached_capacity_adjusted', models.IntegerField(blank=True, null=True)),
                ('cached_capacity_per_day', models.DecimalField(blank=True, decimal_places=7, max_digits=20, null=True)),
                ('capacity_base', models.IntegerField(blank=True, null=True)),
                ('number_of_code_lines_added', models.IntegerField(blank=True, null=True)),
                ('number_of_code_lines_removed', models.IntegerField(blank=True, null=True)),
                ('number_of_code_reviews_submitted', models.IntegerField(blank=True, null=True)),
                ('number_of_comments_made', models.IntegerField(blank=True, null=True)),
                ('number_of_context_switches', models.IntegerField(blank=True, null=True)),
                ('number_of_issues_written', models.IntegerField(blank=True, null=True)),
                ('number_of_paid_time_off_days', models.IntegerField(blank=True, null=True)),
                ('number_of_story_points_committed_to', models.IntegerField(blank=True, null=True)),
                ('number_of_story_points_delivered', models.IntegerField(blank=True, null=True)),
                ('number_of_threads_resolved', models.IntegerField(blank=True, null=True)),
                ('person_developer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.person')),
                ('sprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.sprint')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
