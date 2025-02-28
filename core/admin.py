from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from core.models.acronym import Acronym
from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.client import Client
from core.models.cron_job import CronJob
from core.models.data_point import DataPoint
from core.models.data_use_exception import DataUseException
from core.models.database import Database
from core.models.dependency import Dependency
from core.models.document import Document
from core.models.formula import Formula
from core.models.hotfix import Hotfix
from core.models.incident import Incident
from core.models.job_level import JobLevel
from core.models.link import Link
from core.models.organization import Organization
from core.models.person import Person
from core.models.policy import Policy
from core.models.project import Project
from core.models.release import Release
from core.models.release_bundle import ReleaseBundle
from core.models.report import Report
from core.models.requirement import Requirement
from core.models.risk import Risk
from core.models.role import Role
from core.models.secret import Secret
from core.models.server import Server
from core.models.service_provider import ServiceProvider
from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.models.skill import Skill
from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.models.task import Task
from core.models.team import Team
from core.models.term import Term
from core.models.this_server_configuration import ThisServerConfiguration
from core.models.tool import Tool
from core.models.user import User
from core.models.vulnerability import Vulnerability

admin.site.register(Acronym, SimpleHistoryAdmin)
admin.site.register(Application, SimpleHistoryAdmin)
admin.site.register(ApplicationGroup, SimpleHistoryAdmin)
admin.site.register(Client, SimpleHistoryAdmin)
admin.site.register(CronJob, SimpleHistoryAdmin)
admin.site.register(DataPoint, SimpleHistoryAdmin)
admin.site.register(DataUseException, SimpleHistoryAdmin)
admin.site.register(Database, SimpleHistoryAdmin)
admin.site.register(Dependency, SimpleHistoryAdmin)
admin.site.register(Document, SimpleHistoryAdmin)
admin.site.register(Formula, SimpleHistoryAdmin)
admin.site.register(Hotfix, SimpleHistoryAdmin)
admin.site.register(Incident, SimpleHistoryAdmin)
admin.site.register(JobLevel, SimpleHistoryAdmin)
admin.site.register(Link, SimpleHistoryAdmin)
admin.site.register(Organization, SimpleHistoryAdmin)
admin.site.register(Person, SimpleHistoryAdmin)
admin.site.register(Policy, SimpleHistoryAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(Release, SimpleHistoryAdmin)
admin.site.register(ReleaseBundle, SimpleHistoryAdmin)
admin.site.register(Report, SimpleHistoryAdmin)
admin.site.register(Requirement, SimpleHistoryAdmin)
admin.site.register(Risk, SimpleHistoryAdmin)
admin.site.register(Role, SimpleHistoryAdmin)
admin.site.register(Secret, SimpleHistoryAdmin)
admin.site.register(Server, SimpleHistoryAdmin)
admin.site.register(ServiceProvider, SimpleHistoryAdmin)
admin.site.register(ServiceProviderSecurityRequirementsDocument, SimpleHistoryAdmin)
admin.site.register(Skill, SimpleHistoryAdmin)
admin.site.register(SoftwareBillOfMaterial, SimpleHistoryAdmin)
admin.site.register(Task, SimpleHistoryAdmin)
admin.site.register(Team, SimpleHistoryAdmin)
admin.site.register(Term, SimpleHistoryAdmin)
admin.site.register(ThisServerConfiguration, SimpleHistoryAdmin)
admin.site.register(Tool, SimpleHistoryAdmin)
admin.site.register(User, SimpleHistoryAdmin)
admin.site.register(Vulnerability, SimpleHistoryAdmin)
