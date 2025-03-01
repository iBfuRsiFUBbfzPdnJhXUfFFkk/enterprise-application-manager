# Generated by Django 5.1.6 on 2025-02-28 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_ldap_field_historicaluser_ldap_distinguished_name_dn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='person_mapping',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.person'),
        ),
        migrations.AddField(
            model_name='user',
            name='person_mapping',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_mapping', to='core.person'),
        ),
    ]
