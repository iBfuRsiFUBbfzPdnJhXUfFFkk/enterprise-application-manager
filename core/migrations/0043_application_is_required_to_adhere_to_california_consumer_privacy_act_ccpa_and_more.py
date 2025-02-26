# Generated by Django 5.1.6 on 2025-02-26 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_application_link_whiteboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_required_to_adhere_to_california_consumer_privacy_act_ccpa',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_required_to_adhere_to_general_data_protection_regulation_gdpr',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_required_to_adhere_to_payment_card_industry_data_security_standard_pci_dss',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_storing_nonpublic_personal_information_npi',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_storing_personally_identifiable_information_pii',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_storing_protected_health_information_phi',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='is_using_artificial_intelligence',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
