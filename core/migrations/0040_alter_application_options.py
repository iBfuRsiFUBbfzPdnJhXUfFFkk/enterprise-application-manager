# Generated by Django 5.1.6 on 2025-02-26 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_document_blob_content_type_document_blob_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['name', 'acronym', '-id']},
        ),
    ]
