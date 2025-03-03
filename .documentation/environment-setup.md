# Environment Setup

## Point To The Correct Settings Environment

This needs to be in front of your run command

```bash
export DJANGO_SETTINGS_MODULE="core.settings.local"
```

## ENV File

```properties
ALLOWED_HOSTS=["127.0.0.1","0.0.0.0","localhost"]
AUTH_LDAP_BIND_DN="domain\\username"
AUTH_LDAP_BIND_PASSWORD="password"
AUTH_LDAP_SEARCH_BASE="dc=domain,dc=com"
AUTH_LDAP_SEARCH_FILTER="(AccountName=%(user))"
AUTH_LDAP_SERVER_URI="ldap://ldap.domain.com"
AUTH_LDAP_USER_ATTR_MAP="{\"first_name\": \"firstName\"}"
DEBUG=True
DJANGO_SECRET_KEY="******"
ENCRYPTION_SECRET="******"
SHOULD_USE_LDAP=False
```