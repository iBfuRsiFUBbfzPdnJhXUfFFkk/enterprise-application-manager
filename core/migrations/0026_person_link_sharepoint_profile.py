# Generated by Django 5.1.6 on 2025-02-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_person_is_developer'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='link_sharepoint_profile',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
