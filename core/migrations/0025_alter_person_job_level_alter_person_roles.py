# Generated by Django 5.1.6 on 2025-03-06 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_historicalonboardprocedure_onboardprocedure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='job_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.joblevel'),
        ),
        migrations.AlterField(
            model_name='person',
            name='roles',
            field=models.ManyToManyField(blank=True, to='core.role'),
        ),
    ]
