# Generated by Django 5.1.6 on 2025-03-09 05:19

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0015_alter_gitlabissue_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GitLabIteration',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('iid', models.IntegerField(blank=True, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('web_url', models.CharField(blank=True, max_length=255, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='iterations', to='git_lab.gitlabgroup')),
            ],
            options={
                'verbose_name': 'GitLab Iteration',
                'verbose_name_plural': 'GitLab Iterations',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='iteration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='issues', to='git_lab.gitlabiteration'),
        ),
        migrations.AddField(
            model_name='historicalgitlabissue',
            name='iteration',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabiteration'),
        ),
        migrations.CreateModel(
            name='HistoricalGitLabIteration',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('iid', models.IntegerField(blank=True, null=True)),
                ('id', models.IntegerField(db_index=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('web_url', models.CharField(blank=True, max_length=255, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('group', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabgroup')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '_Historical Record for GitLabIteration',
                'verbose_name_plural': '_Historical Records for GitLabIteration',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
