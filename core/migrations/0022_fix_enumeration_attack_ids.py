import uuid
from django.db import migrations, models

def generate_uuids(apps, schema_editor):
    models_to_update = [
        apps.get_model('core', 'Acronym'),
        apps.get_model('core', 'Action'),
        apps.get_model('core', 'Application'),
        apps.get_model('core', 'ApplicationGroup'),
        apps.get_model('core', 'Client'),
        apps.get_model('core', 'Command'),
        apps.get_model('core', 'CronJob'),
        apps.get_model('core', 'DataPoint'),
        apps.get_model('core', 'DataUseException'),
        apps.get_model('core', 'Database'),
        apps.get_model('core', 'Dependency'),
        apps.get_model('core', 'Document'),
        apps.get_model('core', 'Formula'),
        apps.get_model('core', 'GitLabIteration'),
        apps.get_model('core', 'Hotfix'),
        apps.get_model('core', 'Incident'),
        apps.get_model('core', 'JobLevel'),
        apps.get_model('core', 'Link'),
        apps.get_model('core', 'Organization'),
        apps.get_model('core', 'Person'),
        apps.get_model('core', 'Policy'),
        apps.get_model('core', 'Project'),
        apps.get_model('core', 'Release'),
        apps.get_model('core', 'ReleaseBundle'),
        apps.get_model('core', 'Report'),
        apps.get_model('core', 'Requirement'),
        apps.get_model('core', 'Risk'),
        apps.get_model('core', 'Role'),
        apps.get_model('core', 'Secret'),
        apps.get_model('core', 'Server'),
        apps.get_model('core', 'ServiceProvider'),
        apps.get_model('core', 'ServiceProviderSecurityRequirementsDocument'),
        apps.get_model('core', 'Skill'),
        apps.get_model('core', 'SoftwareBillOfMaterial'),
        apps.get_model('core', 'Sprint'),
        apps.get_model('core', 'Task'),
        apps.get_model('core', 'Team'),
        apps.get_model('core', 'Term'),
        apps.get_model('core', 'ThisServerConfiguration'),
        apps.get_model('core', 'Tool'),
        apps.get_model('core', 'User'),
        apps.get_model('core', 'Vulnerability'),
    ]

    for model in models_to_update:
        for obj in model.objects.all():
            obj.enumeration_attack_uuid = uuid.uuid4()
            obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_historicaluser_enumeration_attack_uuid_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_uuids),
    ]
