# Generated by Django 5.1.6 on 2025-02-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_application_is_legacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='link_gitlab_wiki',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='link_open_ai',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='link_sentry_io',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
