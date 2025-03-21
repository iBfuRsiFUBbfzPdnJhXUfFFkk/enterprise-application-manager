# Generated by Django 5.1.6 on 2025-03-06 01:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_fix_enumeration_attack_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acronym',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='applicationgroup',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='command',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='cronjob',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='database',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='datauseexception',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='formula',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='gitlabiteration',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='historicalacronym',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalaction',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalapplication',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalapplicationgroup',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalclient',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalcommand',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalcronjob',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaldatabase',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaldatapoint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaldatauseexception',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaldependency',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaldocument',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalformula',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalgitlabiteration',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalhotfix',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalincident',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaljoblevel',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicallink',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalpolicy',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalrelease',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalreleasebundle',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalrequirement',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalrisk',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalrole',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalsecret',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalserver',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalserviceprovider',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalserviceprovidersecurityrequirementsdocument',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalskill',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalsoftwarebillofmaterial',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalsprint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaltask',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalteam',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalterm',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalthisserverconfiguration',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaltool',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalvulnerability',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='hotfix',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='joblevel',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='policy',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='releasebundle',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='risk',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='secret',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='serviceprovidersecurityrequirementsdocument',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='softwarebillofmaterial',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='thisserverconfiguration',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='enumeration_attack_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
