# Generated by Django 5.1.6 on 2025-02-26 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_rename_name_pronunciation_person_pronunciation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='acronym',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='acronym',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='policy',
            name='acronym',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
