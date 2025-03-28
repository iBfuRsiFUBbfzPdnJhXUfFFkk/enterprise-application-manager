# Generated by Django 5.1.7 on 2025-03-13 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0031_gitlabmergerequest_group_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitlabdiscussion',
            options={'ordering': ['-updated_at', '-id'], 'verbose_name': 'GitLab Discussion', 'verbose_name_plural': 'GitLab Discussions'},
        ),
        migrations.AddField(
            model_name='gitlabdiscussion',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gitlabdiscussion',
            name='started_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='discussions_started', to='git_lab.gitlabuser'),
        ),
        migrations.AddField(
            model_name='gitlabdiscussion',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabdiscussion',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabdiscussion',
            name='started_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabuser'),
        ),
        migrations.AddField(
            model_name='historicalgitlabdiscussion',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
