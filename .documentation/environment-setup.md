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
EMAIL_FROM="user@domain.com"
EMAIL_HOST="localhost"
EMAIL_PORT=25
EMAIL_USE_SSL=False
EMAIL_USE_TLS=False
ENCRYPTION_SECRET="******"
POPPLER_PATH="C:/Program Files/poppler/bin"
SHOULD_USE_LDAP=False
```

### Environment Variables

#### Required Variables

- **DJANGO_SECRET_KEY** - Django secret key for cryptographic signing
- **ENCRYPTION_SECRET** - Secret key for encrypting sensitive data in the database

#### Optional Variables

- **DEBUG** - Enable debug mode (default: False)
- **ALLOWED_HOSTS** - JSON array of allowed hosts (default: ["localhost", "127.0.0.1"])
- **SHOULD_USE_LDAP** - Enable LDAP authentication (default: False)
- **POPPLER_PATH** - Path to poppler bin directory for PDF to image conversion (optional)
  - Windows: Set to the bin directory, e.g., `C:/Program Files/poppler/bin`
  - Unix/Mac: Leave empty to use system PATH
  - Download poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases/

#### LDAP Variables (if SHOULD_USE_LDAP=True)

- **AUTH_LDAP_SERVER_URI** - LDAP server URI
- **AUTH_LDAP_BIND_DN** - Distinguished name for binding to LDAP
- **AUTH_LDAP_BIND_PASSWORD** - Password for LDAP binding
- **AUTH_LDAP_SEARCH_BASE** - Base DN for user searches
- **AUTH_LDAP_SEARCH_FILTER** - LDAP filter for finding users
- **AUTH_LDAP_USER_ATTR_MAP** - JSON mapping of LDAP attributes to Django user fields

#### Email Variables

- **EMAIL_HOST** - SMTP server hostname
- **EMAIL_PORT** - SMTP server port
- **EMAIL_FROM** - Default "from" email address
- **EMAIL_USE_SSL** - Use SSL for email (default: False)
- **EMAIL_USE_TLS** - Use TLS for email (default: False)