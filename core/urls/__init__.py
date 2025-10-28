from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver, path, include

from core.urls.urlpatterns_acronym import urlpatterns_acronym
from core.urls.urlpatterns_action import urlpatterns_action
from core.urls.urlpatterns_ai_governance import urlpatterns_ai_governance
from core.urls.urlpatterns_ai_hallucination import urlpatterns_ai_hallucination
from core.urls.urlpatterns_ai_use_case import urlpatterns_ai_use_case
from core.urls.urlpatterns_ai_vendor import urlpatterns_ai_vendor
from core.urls.urlpatterns_api import urlpatterns_api
from core.urls.urlpatterns_application import urlpatterns_application
from core.urls.urlpatterns_application_group import urlpatterns_application_group
from core.urls.urlpatterns_billing_code import urlpatterns_billing_code
from core.urls.urlpatterns_client import urlpatterns_client
from core.urls.urlpatterns_command import urlpatterns_command
from core.urls.urlpatterns_cron_job import urlpatterns_cron_job
from core.urls.urlpatterns_data_point import urlpatterns_data_point
from core.urls.urlpatterns_data_use_exception import urlpatterns_data_use_exception
from core.urls.urlpatterns_database import urlpatterns_database
from core.urls.urlpatterns_dependency import urlpatterns_dependency
from core.urls.urlpatterns_document import urlpatterns_document
from core.urls.urlpatterns_estimation import urlpatterns_estimation
from core.urls.urlpatterns_external_blocker import urlpatterns_external_blocker
from core.urls.urlpatterns_formula import urlpatterns_formula
from core.urls.urlpatterns_hotfix import urlpatterns_hotfix
from core.urls.urlpatterns_incident import urlpatterns_incident
from core.urls.urlpatterns_job_level import urlpatterns_job_level
from core.urls.urlpatterns_job_title import urlpatterns_job_title
from core.urls.urlpatterns_link import urlpatterns_link
from core.urls.urlpatterns_login_credential import urlpatterns_login_credential
from core.urls.urlpatterns_onboard_procedure import urlpatterns_onboard_procedure
from core.urls.urlpatterns_login import urlpatterns_login
from core.urls.urlpatterns_logout import urlpatterns_logout
from core.urls.urlpatterns_organization import urlpatterns_organization
from core.urls.urlpatterns_person import urlpatterns_person
from core.urls.urlpatterns_policy import urlpatterns_policy
from core.urls.urlpatterns_profile import urlpatterns_profile
from core.urls.urlpatterns_project import urlpatterns_project
from core.urls.urlpatterns_release import urlpatterns_release
from core.urls.urlpatterns_release_bundle import urlpatterns_release_bundle
from core.urls.urlpatterns_report import urlpatterns_report
from core.urls.urlpatterns_requirement import urlpatterns_requirement
from core.urls.urlpatterns_risk import urlpatterns_risk
from core.urls.urlpatterns_role import urlpatterns_role
from core.urls.urlpatterns_secret import urlpatterns_secret
from core.urls.urlpatterns_server import urlpatterns_server
from core.urls.urlpatterns_server_configuration import urlpatterns_server_configuration
from core.urls.urlpatterns_service_provider import urlpatterns_service_provider
from core.urls.urlpatterns_service_provider_security_requirements_document import urlpatterns_service_provider_security_requirements_document
from core.urls.urlpatterns_skill import urlpatterns_skill
from core.urls.urlpatterns_software_bill_of_material import urlpatterns_software_bill_of_material
from core.urls.urlpatterns_sprint import urlpatterns_sprint
from core.urls.urlpatterns_task import urlpatterns_task
from core.urls.urlpatterns_team import urlpatterns_team
from core.urls.urlpatterns_term import urlpatterns_term
from core.urls.urlpatterns_tool import urlpatterns_tool
from core.urls.urlpatterns_vulnerability import urlpatterns_vulnerability
from core.urls.urlpatterns_settings import urlpatterns_settings
from core.urls.urlpatterns_this_api import urlpatterns_this_api
from core.views import home_view
from kpi.urls import urlpatterns_kpi

urlpatterns_authenticated: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home/", view=home_view),

    # ADMIN
    path(name="admin", route="admin/", view=site.urls),

    path(route='hijack/', view=include(arg='hijack.urls')),

    *urlpatterns_acronym,
    *urlpatterns_action,
    *urlpatterns_ai_governance,
    *urlpatterns_ai_hallucination,
    *urlpatterns_ai_use_case,
    *urlpatterns_ai_vendor,
    *urlpatterns_application,
    *urlpatterns_application_group,
    *urlpatterns_billing_code,
    *urlpatterns_client,
    *urlpatterns_command,
    *urlpatterns_cron_job,
    *urlpatterns_data_point,
    *urlpatterns_data_use_exception,
    *urlpatterns_database,
    *urlpatterns_dependency,
    *urlpatterns_document,
    *urlpatterns_estimation,
    *urlpatterns_external_blocker,
    *urlpatterns_formula,
    *urlpatterns_hotfix,
    *urlpatterns_incident,
    *urlpatterns_job_level,
    *urlpatterns_job_title,
    *urlpatterns_link,
    *urlpatterns_login_credential,
    *urlpatterns_onboard_procedure,
    *urlpatterns_logout,
    *urlpatterns_organization,
    *urlpatterns_person,
    *urlpatterns_policy,
    *urlpatterns_profile,
    *urlpatterns_project,
    *urlpatterns_release,
    *urlpatterns_release_bundle,
    *urlpatterns_report,
    *urlpatterns_requirement,
    *urlpatterns_risk,
    *urlpatterns_role,
    *urlpatterns_secret,
    *urlpatterns_server,
    *urlpatterns_server_configuration,
    *urlpatterns_service_provider,
    *urlpatterns_service_provider_security_requirements_document,
    *urlpatterns_settings,
    *urlpatterns_skill,
    *urlpatterns_software_bill_of_material,
    *urlpatterns_sprint,
    *urlpatterns_task,
    *urlpatterns_team,
    *urlpatterns_term,
    *urlpatterns_this_api,
    *urlpatterns_tool,
    *urlpatterns_vulnerability,
    path(name="kpi", route='kpi/', view=include(arg=(urlpatterns_kpi, 'kpi'), namespace="kpi")),
    *urlpatterns_api
]

urlpatterns: list[URLPattern | URLResolver] = [
    path(name="index", route="", view=login_required(function=home_view)),
    *urlpatterns_login,
    path(name="authenticated", route='authenticated/', view=include(arg=urlpatterns_authenticated)),
]
