# Generated by Django 5.1.6 on 2025-03-09 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0012_gitlabissue_historicalgitlabissue'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabissue',
            name='link_award_emoji',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='link_notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='link_project',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='link_self',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabissue',
            name='link_award_emoji',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabissue',
            name='link_notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabissue',
            name='link_project',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalgitlabissue',
            name='link_self',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
