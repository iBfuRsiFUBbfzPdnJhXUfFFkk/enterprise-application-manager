# Generated by Django 5.1.6 on 2025-02-26 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='blob_content_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='blob_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
