# Generated by Django 5.1.6 on 2025-03-07 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_jobtitle_historicaljobtitle_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['name', '-id'], 'verbose_name': 'Role', 'verbose_name_plural': 'Roles'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['name', '-id'], 'verbose_name': 'Skill', 'verbose_name_plural': 'Skills'},
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='communication_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='communication_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='skills',
            field=models.ManyToManyField(blank=True, to='core.skill'),
        ),
    ]
