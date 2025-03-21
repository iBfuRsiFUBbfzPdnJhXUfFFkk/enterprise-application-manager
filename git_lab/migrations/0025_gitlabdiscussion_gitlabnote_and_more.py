# Generated by Django 5.1.7 on 2025-03-12 18:51

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0024_gitlabchange_scrum_sprint_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GitLabDiscussion',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('individual_note', models.BooleanField(blank=True, default=False, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='discussions', to='git_lab.gitlabproject')),
            ],
            options={
                'verbose_name': 'GitLab Discussion',
                'verbose_name_plural': 'GitLab Discussions',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GitLabNote',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('noteable_id', models.IntegerField(blank=True, null=True)),
                ('noteable_iid', models.IntegerField(blank=True, null=True)),
                ('noteable_type', models.CharField(blank=True, max_length=255, null=True)),
                ('system', models.BooleanField(blank=True, default=False, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notes_authored', to='git_lab.gitlabuser')),
                ('discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notes', to='git_lab.gitlabdiscussion')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notes', to='git_lab.gitlabproject')),
            ],
            options={
                'verbose_name': 'GitLab Note',
                'verbose_name_plural': 'GitLab Notes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalGitLabDiscussion',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False)),
                ('id', models.CharField(db_index=True, max_length=40)),
                ('individual_note', models.BooleanField(blank=True, default=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabproject')),
            ],
            options={
                'verbose_name': '_Historical Record for GitLabDiscussion',
                'verbose_name_plural': '_Historical Records for GitLabDiscussion',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGitLabNote',
            fields=[
                ('enumeration_attack_uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.IntegerField(db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('noteable_id', models.IntegerField(blank=True, null=True)),
                ('noteable_iid', models.IntegerField(blank=True, null=True)),
                ('noteable_type', models.CharField(blank=True, max_length=255, null=True)),
                ('system', models.BooleanField(blank=True, default=False, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabuser')),
                ('discussion', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabdiscussion')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabproject')),
            ],
            options={
                'verbose_name': '_Historical Record for GitLabNote',
                'verbose_name_plural': '_Historical Records for GitLabNote',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
