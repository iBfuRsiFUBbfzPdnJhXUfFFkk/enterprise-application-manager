#!/usr/bin/env python
"""
Diagnostic script to check AIUseCase model and database state.
Run this on the other computer to diagnose the KeyError issue.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
django.setup()

from django.db import connection
from core.models.ai_use_case import AIUseCase

print("=" * 80)
print("DIAGNOSTIC REPORT: AIUseCase Model and Database")
print("=" * 80)

# 1. Check model fields
print("\n1. MODEL FIELDS DEFINED IN CODE:")
print("-" * 80)
model_fields = [f.name for f in AIUseCase._meta.get_fields() if not f.name.startswith('historical')]
for field in sorted(model_fields):
    print(f"  - {field}")
print(f"\nTotal fields in model: {len(model_fields)}")

# 2. Check database columns
print("\n2. DATABASE COLUMNS IN core_aiusecase TABLE:")
print("-" * 80)
with connection.cursor() as cursor:
    # Get database engine
    db_engine = connection.settings_dict['ENGINE']
    print(f"Database engine: {db_engine}")

    if 'sqlite' in db_engine:
        # SQLite
        cursor.execute("PRAGMA table_info(core_aiusecase)")
        db_columns = [row[1] for row in cursor.fetchall()]
    elif 'postgresql' in db_engine:
        # PostgreSQL
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'core_aiusecase'
            ORDER BY ordinal_position
        """)
        db_columns = [row[0] for row in cursor.fetchall()]
    elif 'mysql' in db_engine:
        # MySQL
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'core_aiusecase'
            ORDER BY ordinal_position
        """)
        db_columns = [row[0] for row in cursor.fetchall()]
    else:
        print(f"⚠️  Unsupported database engine: {db_engine}")
        db_columns = []

for column in db_columns:
    print(f"  - {column}")
print(f"\nTotal columns in database: {len(db_columns)}")

# 3. Check for mismatches
print("\n3. MISMATCH ANALYSIS:")
print("-" * 80)
model_field_names = set(model_fields)
db_column_names = set(db_columns)

extra_in_db = db_column_names - model_field_names
extra_in_model = model_field_names - db_column_names

if extra_in_db:
    print(f"\n⚠️  COLUMNS IN DATABASE BUT NOT IN MODEL ({len(extra_in_db)}):")
    for col in sorted(extra_in_db):
        print(f"  - {col}")
else:
    print("\n✅ No extra columns in database")

if extra_in_model:
    print(f"\n⚠️  FIELDS IN MODEL BUT NOT IN DATABASE ({len(extra_in_model)}):")
    for field in sorted(extra_in_model):
        print(f"  - {field}")
else:
    print("\n✅ No missing columns in database")

# 4. Check migration status
print("\n4. MIGRATION STATUS:")
print("-" * 80)
from django.db.migrations.executor import MigrationExecutor
executor = MigrationExecutor(connection)
targets = executor.loader.graph.leaf_nodes()
plan = executor.migration_plan(targets)

if plan:
    print("⚠️  UNAPPLIED MIGRATIONS:")
    for migration, backwards in plan:
        print(f"  - {migration.app_label}.{migration.name}")
else:
    print("✅ All migrations applied")

# Check specifically for 0052
from django.db.migrations.recorder import MigrationRecorder
recorder = MigrationRecorder(connection)
applied_migrations = list(recorder.applied_migrations())
migration_0052 = ('core', '0052_remove_ai_use_case_federal_compliance_fields')
if migration_0052 in applied_migrations:
    print(f"\n✅ Migration 0052 (removal) is applied")
else:
    print(f"\n⚠️  Migration 0052 (removal) is NOT applied")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
