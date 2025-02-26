from django.contrib import admin

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
from core.models.link import Link
from core.models.organization import Organization
from core.models.person import Person
from core.models.policy import Policy
from core.models.release import Release
from core.models.release_bundle import ReleaseBundle
from core.models.requirement import Requirement
from core.models.risk import Risk
from core.models.role import Role
from core.models.secret import Secret
from core.models.server import Server
from core.models.service_provider import ServiceProvider
from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.models.task import Task
from core.models.team import Team
from core.models.term import Term
from core.models.tool import Tool
from core.models.vulnerability import Vulnerability

admin.site.register(Acronym)
admin.site.register(Application)
admin.site.register(ApplicationGroup)
admin.site.register(Client)
admin.site.register(CronJob)
admin.site.register(DataPoint)
admin.site.register(DataUseException)
admin.site.register(Database)
admin.site.register(Dependency)
admin.site.register(Document)
admin.site.register(Formula)
admin.site.register(Hotfix)
admin.site.register(Incident)
admin.site.register(Link)
admin.site.register(Organization)
admin.site.register(Person)
admin.site.register(Policy)
admin.site.register(Release)
admin.site.register(ReleaseBundle)
admin.site.register(Requirement)
admin.site.register(Risk)
admin.site.register(Role)
admin.site.register(Secret)
admin.site.register(Server)
admin.site.register(ServiceProvider)
admin.site.register(ServiceProviderSecurityRequirementsDocument)
admin.site.register(SoftwareBillOfMaterial)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Term)
admin.site.register(Tool)
admin.site.register(Vulnerability)
