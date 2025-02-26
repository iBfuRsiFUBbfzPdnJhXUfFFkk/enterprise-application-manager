# Generated by Django 5.1.6 on 2025-02-26 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_database_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(blank=True, max_length=255, null=True)),
                ('blob_data', models.BinaryField(blank=True, null=True)),
                ('blob_filename', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
