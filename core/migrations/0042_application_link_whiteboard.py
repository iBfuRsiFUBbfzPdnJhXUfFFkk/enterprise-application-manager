# Generated by Django 5.1.6 on 2025-02-26 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_alter_applicationgroup_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='link_whiteboard',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
