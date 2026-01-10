# noinspection PyUnresolvedReferences
from core.settings.common.authentication import *
# noinspection PyUnresolvedReferences
from core.settings.common.developer import *
# noinspection PyUnresolvedReferences
from core.settings.common.email import *
# noinspection PyUnresolvedReferences
from core.settings.common.installed_apps import *
# noinspection PyUnresolvedReferences
from core.settings.common.internationalization import *
# noinspection PyUnresolvedReferences
from core.settings.common.ldap import *
# noinspection PyUnresolvedReferences
from core.settings.common.middleware import *
# noinspection PyUnresolvedReferences
from core.settings.common.models import *
# noinspection PyUnresolvedReferences
from core.settings.common.security import *
# noinspection PyUnresolvedReferences
from core.settings.common.templates import *
# noinspection PyUnresolvedReferences
from core.settings.common.urls_and_directories import *
# noinspection PyUnresolvedReferences
from core.settings.common.storage import *
# noinspection PyUnresolvedReferences
from core.settings.common.webauthn import *

# https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
WSGI_APPLICATION = 'core.wsgi.application'
