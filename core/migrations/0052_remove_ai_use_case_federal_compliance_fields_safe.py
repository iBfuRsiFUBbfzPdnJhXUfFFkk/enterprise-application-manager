# Generated manually to safely remove AI use case federal compliance fields

from django.db import migrations, connection


def get_table_columns(table_name):
    """Get list of columns for a table."""
    with connection.cursor() as cursor:
        db_engine = connection.settings_dict['ENGINE']

        if 'sqlite' in db_engine:
            cursor.execute(f"PRAGMA table_info({table_name})")
            return [row[1] for row in cursor.fetchall()]
        elif 'postgresql' in db_engine:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
            """, [table_name])
            return [row[0] for row in cursor.fetchall()]
        elif 'mysql' in db_engine:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
            """, [table_name])
            return [row[0] for row in cursor.fetchall()]
    return []


def drop_column_if_exists(schema_editor, table_name, column_name):
    """Drop a column if it exists in the table."""
    existing_columns = get_table_columns(table_name)

    if column_name not in existing_columns:
        print(f"  Skipping {table_name}.{column_name} (does not exist)")
        return

    db_engine = connection.settings_dict['ENGINE']

    if 'sqlite' in db_engine:
        # SQLite doesn't support DROP COLUMN easily, would need to recreate table
        # For SQLite, we'll use Django's schema editor
        print(f"  Dropping {table_name}.{column_name} (SQLite - using schema editor)")
        # We can't easily drop columns in SQLite without knowing the full table structure
        # So we'll just skip for SQLite - the fields will be ignored by Django anyway
        print(f"  WARNING: Cannot drop column in SQLite. Column will be orphaned but ignored by Django.")
    else:
        # PostgreSQL and MySQL support DROP COLUMN
        with connection.cursor() as cursor:
            print(f"  Dropping {table_name}.{column_name}")
            cursor.execute(f'ALTER TABLE {table_name} DROP COLUMN {column_name}')


def remove_fields_forward(apps, schema_editor):
    """Remove the federal compliance fields if they exist."""
    print("\nRemoving AI use case federal compliance fields (if they exist)...")

    fields_to_remove = [
        'affected_groups_consultation_steps',
        'agency_has_code_access',
        'agency_owned_training_data_description',
        'ai_impact_assessment_conducted',
        'ai_system_outputs_description',
        'ai_use_notice_approach',
        'ato_system_name',
        'caio_determination_justification',
        'can_ai_act_without_human_involvement',
        'client_id',
        'contact_email',
        'contact_name',
        'data_science_tools_reuse_approach',
        'date_deployed',
        'date_development_or_acquisition_began',
        'date_initiated',
        'date_retired',
        'demographic_variables_used',
        'developed_under_contract_or_inhouse',
        'development_lifecycle_stage',
        'disparities_detection_mitigation_steps',
        'disseminates_info_to_public',
        'has_access_to_enterprise_data_catalog',
        'has_ato_for_ai_system',
        'has_computing_resources_request_process',
        'has_fallback_and_escalation_process',
        'has_model_training_data_documentation',
        'has_opt_out_mechanism',
        'has_post_deployment_monitoring_process',
        'hisp_supporting',
        'includes_custom_developed_code',
        'independent_evaluation_conducted',
        'info_made_available_for_review',
        'info_quality_act_compliance_approach',
        'intended_purpose_and_benefits',
        'involves_pii_maintained_by_client',
        'is_currently_active',
        'is_in_commercial_ai_products_list',
        'is_provisioning_communication_timely',
        'is_rights_impacting',
        'is_safety_impacting',
        'is_used_for_decisions_with_adverse_impact',
        'it_infrastructure_provisioning_method',
        'key_risks_and_identification_method',
        'open_source_code_url',
        'presumed_rights_impacting_category',
        'presumed_safety_impacting_category',
        'procurement_instrument_identifiers',
        'public_facing_service_supporting',
        'requested_extension_for_risk_management',
        'saop_assessed_privacy_risks',
        'summary',
        'supports_hisp_public_facing_service',
        'tested_in_operational_environment',
        'use_case_topic_area',
        'uses_face_recognition_or_capture',
        'wait_time_for_developer_tools',
    ]

    # Drop from core_aiusecase
    print("\nProcessing core_aiusecase table:")
    for field in fields_to_remove:
        drop_column_if_exists(schema_editor, 'core_aiusecase', field)

    # Drop from core_historicalaiusecase
    print("\nProcessing core_historicalaiusecase table:")
    for field in fields_to_remove:
        drop_column_if_exists(schema_editor, 'core_historicalaiusecase', field)

    print("\nMigration complete!")


def remove_fields_reverse(apps, schema_editor):
    """
    Reverse migration - this is intentionally left empty.
    We cannot recreate the fields without knowing their exact definitions.
    If you need to reverse this, restore from backup.
    """
    print("WARNING: Reverse migration not implemented. Restore from backup if needed.")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_aivendor_aigovernance_aiusecase_aihallucination_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_fields_forward, remove_fields_reverse),
    ]
