# Generated by Django 5.1.7 on 2025-03-13 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_lab', '0026_gitlabnote_scrum_sprint_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitlabchange',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Change', 'verbose_name_plural': 'GitLab Changes'},
        ),
        migrations.AlterModelOptions(
            name='gitlabgroup',
            options={'ordering': ['-created_at'], 'verbose_name': 'GitLab Group', 'verbose_name_plural': 'GitLab Groups'},
        ),
        migrations.AlterModelOptions(
            name='gitlabissue',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Issue', 'verbose_name_plural': 'GitLab Issues'},
        ),
        migrations.AlterModelOptions(
            name='gitlabiteration',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Iteration', 'verbose_name_plural': 'GitLab Iterations'},
        ),
        migrations.AlterModelOptions(
            name='gitlabmergerequest',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Merge Request', 'verbose_name_plural': 'GitLab Merge Requests'},
        ),
        migrations.AlterModelOptions(
            name='gitlabnote',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Note', 'verbose_name_plural': 'GitLab Notes'},
        ),
        migrations.AlterModelOptions(
            name='gitlabproject',
            options={'ordering': ['-updated_at'], 'verbose_name': 'GitLab Project', 'verbose_name_plural': 'GitLab Projects'},
        ),
        migrations.AlterModelOptions(
            name='gitlabuser',
            options={'ordering': ['-created_at'], 'verbose_name': 'GitLab User', 'verbose_name_plural': 'GitLab Users'},
        ),
    ]
