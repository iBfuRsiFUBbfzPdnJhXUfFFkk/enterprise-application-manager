# Generated by Django 5.1.7 on 2025-03-13 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0034_gitlabnote_web_url_historicalgitlabnote_web_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabnote',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabnote',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
