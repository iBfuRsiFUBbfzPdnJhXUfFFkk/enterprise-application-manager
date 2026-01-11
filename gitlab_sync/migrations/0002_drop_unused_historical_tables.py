# Generated manually to drop Historical tables for models with _disable_history = True

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitlab_sync', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncartifact;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncbranch;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsynccommit;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncepic;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncevent;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncgroup;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncissue;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsynciteration;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncjob;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncjobtracker;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncmergerequest;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncmilestone;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncpipeline;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncproject;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncrepository;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncsecurityreport;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncsnippet;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsynctag;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncuser;",
                "DROP TABLE IF EXISTS gitlab_sync_historicalgitlabsyncvulnerability;",
            ],
            reverse_sql=[
                # Dropping tables is irreversible - raise an error if attempting to reverse
                "SELECT 'Cannot recreate dropped historical tables. Restore from backup if needed.';"
            ],
        ),
    ]
