# Generated by Django 5.1.7 on 2025-03-11 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0012_historicalkeyperformanceindicatorsprint_git_lab_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyperformanceindicatorsprint',
            options={'ordering': ['-scrum_sprint__date_end', '-sprint__date_end', '-id'], 'verbose_name': 'Key Performance Indicator (KPI) Sprint', 'verbose_name_plural': 'Key Performance Indicator (KPI) Sprints'},
        ),
    ]
