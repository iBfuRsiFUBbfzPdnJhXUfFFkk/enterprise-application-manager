# Generated by Django 5.1.6 on 2025-02-25 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_application_application_downstream_dependencies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='acronym',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='is_externally_facing',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='link_development_server',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='link_gitlab_repository',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='link_production_server',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='link_production_server_external',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='link_staging_server',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='link_gitlab_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name_first',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name_last',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
