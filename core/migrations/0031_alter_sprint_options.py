# Generated by Django 5.1.6 on 2025-03-07 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_alter_historicalacronym_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sprint',
            options={'ordering': ['-date_end', '-id'], 'verbose_name': 'Sprint', 'verbose_name_plural': 'Sprints'},
        ),
    ]
