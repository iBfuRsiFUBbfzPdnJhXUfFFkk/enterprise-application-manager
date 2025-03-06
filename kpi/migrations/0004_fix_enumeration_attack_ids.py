import uuid
from django.db import migrations, models

def generate_uuids(apps, schema_editor):
    models_to_update = [
        apps.get_model('kpi', 'KeyPerformanceIndicatorSprint'),
    ]

    for model in models_to_update:
        for obj in model.objects.all():
            obj.enumeration_attack_uuid = uuid.uuid4()
            obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0003_rename_number_of_threads_resolved_historicalkeyperformanceindicatorsprint_number_of_threads_made_and'),
    ]

    operations = [
        migrations.RunPython(generate_uuids),
    ]
