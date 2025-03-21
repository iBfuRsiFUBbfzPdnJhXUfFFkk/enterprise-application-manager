# Generated by Django 5.1.6 on 2025-03-07 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_role_options_alter_skill_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalsprint',
            old_name='cached_number_of_code_reviews',
            new_name='cached_total_number_of_merge_requests_approved',
        ),
        migrations.RenameField(
            model_name='historicalsprint',
            old_name='cached_number_of_story_points_delivered',
            new_name='cached_total_number_of_story_points_delivered',
        ),
        migrations.RenameField(
            model_name='sprint',
            old_name='cached_number_of_code_reviews',
            new_name='cached_total_number_of_merge_requests_approved',
        ),
        migrations.RenameField(
            model_name='sprint',
            old_name='cached_number_of_story_points_delivered',
            new_name='cached_total_number_of_story_points_delivered',
        ),
        migrations.AddField(
            model_name='historicalsprint',
            name='cached_total_adjusted_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsprint',
            name='cached_total_number_of_story_points_committed_to',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sprint',
            name='cached_total_adjusted_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sprint',
            name='cached_total_number_of_story_points_committed_to',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
