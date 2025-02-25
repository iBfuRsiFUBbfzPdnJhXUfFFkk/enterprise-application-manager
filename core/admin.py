from django.contrib import admin

from core.models.application import Application
from core.models.database import Database
from core.models.dependency import Dependency
from core.models.person import Person
from core.models.release import Release
from core.models.release_bundle import ReleaseBundle

admin.site.register(Application)
admin.site.register(Database)
admin.site.register(Dependency)
admin.site.register(Person)
admin.site.register(Release)
admin.site.register(ReleaseBundle)
