# Generated by Django 5.1.6 on 2025-03-09 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0007_rename_membership_state_gitlabuser_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlabgroup',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gitlabmergerequest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gitlabproject',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgitlabgroup',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgitlabmergerequest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgitlabproject',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
