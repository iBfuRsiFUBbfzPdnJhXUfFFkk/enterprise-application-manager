# Generated by Django 5.1.7 on 2025-03-10 22:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0016_gitlabiteration_gitlabissue_iteration_and_more'),
        ('scrum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabiteration',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='iterations', to='scrum.scrumsprint'),
        ),
        migrations.AddField(
            model_name='historicalgitlabiteration',
            name='sprint',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='scrum.scrumsprint'),
        ),
    ]
