# Generated by Django 5.1.6 on 2025-03-04 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_historicalthisserverconfiguration_connection_gitlab_api_version_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlabiteration',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='git_lab_iterations', to='core.sprint'),
        ),
    ]
