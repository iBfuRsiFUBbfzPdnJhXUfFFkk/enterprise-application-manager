# Generated by Django 5.1.6 on 2025-02-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_application_person_stakeholders_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_stakeholder',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
