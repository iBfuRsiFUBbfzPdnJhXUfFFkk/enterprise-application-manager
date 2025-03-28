# Generated by Django 5.1.6 on 2025-03-08 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0002_gitlabproject_historicalgitlabproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabproject',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='git_lab.gitlabgroup'),
        ),
        migrations.AddField(
            model_name='historicalgitlabproject',
            name='group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='git_lab.gitlabgroup'),
        ),
    ]
