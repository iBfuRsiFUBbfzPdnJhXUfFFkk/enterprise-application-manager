# Generated by Django 5.1.6 on 2025-02-26 23:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_joblevel_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='job_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='people_who_hold_this_job_level', to='core.joblevel'),
        ),
        migrations.AddField(
            model_name='person',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='people_who_hold_this_skill', to='core.skill'),
        ),
    ]
