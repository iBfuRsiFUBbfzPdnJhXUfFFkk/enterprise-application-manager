# Generated by Django 5.1.7 on 2025-03-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0033_gitlabproject_should_skip_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabnote',
            name='web_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabnote',
            name='web_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
