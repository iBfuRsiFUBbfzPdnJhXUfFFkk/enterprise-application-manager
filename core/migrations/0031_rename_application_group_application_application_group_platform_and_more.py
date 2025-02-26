# Generated by Django 5.1.6 on 2025-02-25 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_applicationgroup_application_application_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='application_group',
            new_name='application_group_platform',
        ),
        migrations.AddField(
            model_name='application',
            name='application_groups',
            field=models.ManyToManyField(blank=True, to='core.applicationgroup'),
        ),
        migrations.AddField(
            model_name='applicationgroup',
            name='is_platform',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
