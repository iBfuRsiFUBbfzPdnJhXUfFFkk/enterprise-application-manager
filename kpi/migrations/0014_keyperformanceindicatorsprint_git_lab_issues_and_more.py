# Generated by Django 5.1.7 on 2025-03-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0019_remove_gitlabmergerequest_iteration_and_more'),
        ('kpi', '0013_alter_keyperformanceindicatorsprint_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyperformanceindicatorsprint',
            name='git_lab_issues',
            field=models.ManyToManyField(blank=True, related_name='kpi_sprints', to='git_lab.gitlabissue'),
        ),
        migrations.AddField(
            model_name='keyperformanceindicatorsprint',
            name='git_lab_iterations',
            field=models.ManyToManyField(blank=True, related_name='kpi_sprints', to='git_lab.gitlabiteration'),
        ),
    ]
