from json import loads

from core.settings.common.environment import env

BACKEND_BUILDER: list[str] = []
SHOULD_USE_LDAP: bool = env.bool(default=False, var='SHOULD_USE_LDAP')
if SHOULD_USE_LDAP is True:
    try:
        from django_auth_ldap.config import LDAPSearch

        BACKEND_BUILDER.append('django_auth_ldap.backend.LDAPBackend')
        AUTH_LDAP_SERVER_URI: str = env(var='AUTH_LDAP_SERVER_URI')
        AUTH_LDAP_BIND_DN: str = env(var='AUTH_LDAP_BIND_DN')
        AUTH_LDAP_BIND_PASSWORD: str = env(var='AUTH_LDAP_BIND_PASSWORD')
        AUTH_LDAP_SEARCH_BASE: str = env(var='AUTH_LDAP_SEARCH_BASE')
        AUTH_LDAP_SEARCH_FILTER: str = env(var='AUTH_LDAP_SEARCH_FILTER')
        AUTH_LDAP_USER_SEARCH: LDAPSearch = LDAPSearch(
            base_dn=AUTH_LDAP_SEARCH_BASE,
            filterstr=AUTH_LDAP_SEARCH_FILTER,
            scope="SUBTREE",
        )
        AUTH_LDAP_USER_ATTR_MAP: dict[str, str] = loads(s=env(default='{}', var='AUTH_LDAP_USER_ATTR_MAP'))
        AUTH_LDAP_ALWAYS_UPDATE_USER: bool = True
    except ImportError:
        raise ImportError(
            "LDAP packages are not installed. Please install them with: "
            "pip install django-auth-ldap python-ldap, or set SHOULD_USE_LDAP=False"
        )
