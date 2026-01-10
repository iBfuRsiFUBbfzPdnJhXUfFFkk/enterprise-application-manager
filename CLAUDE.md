# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Enterprise Application Manager is a Django-based web application designed to help organizations manage large amounts of custom applications. It integrates with GitLab to track projects, issues, merge requests, and provides Scrum/Agile management capabilities along with KPI tracking.

## Development Environment Setup

### Migrating from Virtual Environment to Docker Compose

If you're migrating from the old virtual environment setup to Docker Compose:

1. **Move the database file:**
   ```bash
   mkdir -p data
   mv db.sqlite3 data/db.sqlite3
   ```

2. **Remove the virtual environment (optional):**
   ```bash
   rm -rf .venv
   ```

3. **Start Docker Compose:**
   ```bash
   docker compose up
   ```

### Docker Compose

The application runs using Docker Compose with three services:
- **web** - Django application (Python 3.13)
- **minio** - S3-compatible object storage for media files
- **nginx** - Reverse proxy with SSL termination (HTTPS on port 50478)

### Required Environment Variables

Create a `.env` file in the root directory with these variables (see `.documentation/environment-setup.md` for details):

**Django Configuration:**
- `DJANGO_SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - JSON array of allowed hosts
- `ENCRYPTION_SECRET` - Encryption key for sensitive data
- `SHOULD_USE_LDAP` - Enable LDAP authentication (True/False, defaults to False)
- LDAP configuration (`AUTH_LDAP_*` variables) if using LDAP
- Email configuration (`EMAIL_*` variables)
- `CSRF_TRUSTED_ORIGINS_EXTRA` - Additional CSRF trusted origins (optional)

**MinIO Configuration:**
- `MINIO_ROOT_USER` - MinIO admin username
- `MINIO_ROOT_PASSWORD` - MinIO admin password
- `MINIO_ACCESS_KEY` - Application access key
- `MINIO_SECRET_KEY` - Application secret key
- `MINIO_BUCKET_NAME` - Bucket name (defaults to 'enterprise-app-media')
- `MINIO_ENDPOINT` - MinIO endpoint (defaults to 'minio:9000')
- `MINIO_USE_SSL` - Use SSL for MinIO (defaults to false)
- `USE_MINIO` - Enable MinIO storage backend (defaults to true)

Available Django settings modules (set via `DJANGO_SETTINGS_MODULE`):
- `core.settings.local` - Local development (default in docker-compose.yml)
- `core.settings.development` - Development environment
- `core.settings.staging` - Staging environment
- `core.settings.production` - Production environment

## Common Commands

### Running the Development Server

**Start all services:**
```bash
docker compose up
```

**Start in detached mode (background):**
```bash
docker compose up -d
```

**Stop all services:**
```bash
docker compose down
```

**Rebuild and restart (after dependency changes):**
```bash
docker compose up --build
```

**View logs:**
```bash
docker compose logs -f web
```

**Access points:**
- Django Application (HTTPS): https://localhost:50478
- MinIO Console: http://localhost:9005
- MinIO S3 API: http://localhost:9004

### Database Operations

Run migrations:
```bash
docker compose exec web python manage.py migrate
```

Create new migrations:
```bash
docker compose exec web python manage.py makemigrations
```

Dump database to JSON:
```bash
docker compose exec web python manage.py dumpdata --indent=2 > data.json
```

Load database from JSON:
```bash
docker compose exec web python manage.py loaddata data.json
```

**Note:** The database file is persisted at `./data/db.sqlite3` on the host machine.

### Package Management

**Adding Python dependencies:**
1. Add the package to `requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker compose up --build
   ```

**Adding Node.js dependencies (for Tailwind CSS):**
1. Add the package to `package.json`
2. Rebuild the Docker image:
   ```bash
   docker compose up --build
   ```

**Freeze current Python packages (if needed):**
```bash
docker compose exec web pip freeze > requirements.txt
```

**Note:** The Docker image includes full LDAP support. Python dependencies are installed during the Docker build process from `requirements.txt`.

### Testing

Run a specific test:
```bash
docker compose exec web python manage.py test <app_name>.tests.<test_file>.<TestClass>.<test_method>
```

Run all tests for an app:
```bash
docker compose exec web python manage.py test <app_name>
```

### Docker Management

**Access Django shell:**
```bash
docker compose exec web python manage.py shell
```

**Access container bash:**
```bash
docker compose exec web bash
```

**Rebuild Tailwind CSS:**
```bash
docker compose exec web npm run build:css
```

**Collect static files:**
```bash
docker compose exec web python manage.py collectstatic --noinput
```

## Architecture

### Container Architecture

The application runs in a Docker Compose environment with three interconnected services:

**1. web (Django Application)**
- Based on Python 3.13 slim image
- Includes Node.js 20.x for Tailwind CSS compilation
- Automatically runs `collectstatic` on startup via `docker-entrypoint.sh`
- Hot-reload enabled with volume mounts
- Exposes port 8000 internally (proxied by nginx)
- Persistent database at `./data/db.sqlite3`

**2. minio (S3-Compatible Object Storage)**
- MinIO server for media file storage
- Console UI available at http://localhost:9005
- S3 API available at http://localhost:9004
- Data persisted at `./data/minio`
- Health checks ensure service availability before Django starts

**3. nginx (Reverse Proxy)**
- Alpine-based nginx for SSL termination
- HTTPS available at https://localhost:50478
- SSL certificates expected in `./certs` directory
- Serves static files from `./staticfiles`
- Proxies requests to Django web service

All services communicate via the `enterprise-network` bridge network.

### Django Apps Structure

The project consists of four main Django apps:

1. **core** - The main application containing:
   - Base models (Application, Person, Organization, etc.)
   - Authentication and authorization (supports LDAP)
   - Shared utilities and middleware
   - Global settings configuration split into modular files under `core/settings/common/`
   - URL routing and views
   - Admin interface customization

2. **git_lab** - GitLab integration:
   - Models for GitLab entities (Projects, Issues, MergeRequests, Groups, Users, Changes, Discussions, Notes)
   - API endpoints to sync data from GitLab using `python-gitlab` library
   - Tracks GitLab iterations and maps them to Scrum sprints

3. **scrum** - Agile/Scrum management:
   - Models for ScrumSprint, ScrumStory, ScrumWish
   - Sprint planning and tracking
   - Links to GitLab data for sprint metrics (merge requests, issues, code changes)

4. **kpi** - Key Performance Indicator tracking:
   - KPI models and calculations
   - Sprint-based metrics
   - API endpoints for KPI data

### Settings Architecture

Settings are organized in a modular way under `core/settings/`:
- `base.py` - Imports all common settings modules
- `common/` directory contains:
  - `authentication.py` - Authentication backends
  - `developer.py` - Developer-specific settings
  - `email.py` - Email configuration
  - `installed_apps.py` - INSTALLED_APPS list
  - `internationalization.py` - i18n settings
  - `ldap.py` - LDAP configuration
  - `middleware.py` - Middleware configuration
  - `models.py` - Model settings
  - `security.py` - Security settings
  - `templates.py` - Template configuration
  - `urls_and_directories.py` - URL and directory paths

### Model Patterns

Models use `django-generic-model-fields` for consistent field creation:
- `create_generic_fk()` - Foreign keys
- `create_generic_m2m()` - Many-to-many relationships
- `create_generic_varchar()` - Character fields
- `create_generic_integer()` - Integer fields
- `create_generic_boolean()` - Boolean fields
- `create_generic_date()` / `create_generic_datetime()` - Date/datetime fields
- `create_generic_enum()` - Enum fields with choices

Models inherit from abstract base classes:
- `AbstractBaseModel` - Common base functionality
- `AbstractName` / `AbstractAcronym` / `AbstractAlias` - Naming fields
- `AbstractComment` - Comment field
- `AbstractStartEndDates` - Start/end date fields
- `AbstractGitLab*` - GitLab-specific abstract models (in `git_lab/models/common/abstract/`)

All models use `django-simple-history` for historical tracking (creates `Historical*` model variants).

### Form Patterns

**IMPORTANT: Automatic Form Styling**

All forms inherit from `BaseModelForm` which automatically applies Tailwind CSS classes to form widgets. This ensures consistent, visible styling across all forms without manual CSS class definitions.

- **DO NOT** manually add CSS classes to basic form widgets - they are added automatically
- The `BaseModelForm.__init__()` method applies appropriate Tailwind classes based on widget type:
  - Text inputs, number inputs, email, URL, date/time inputs: Full-width with border, shadow, and focus states
  - Textareas: Same styling as text inputs
  - Select dropdowns: Consistent with text inputs
  - Checkboxes: Smaller, rounded with blue accent
  - File inputs: Consistent with text inputs
- If custom classes are needed, add them to the widget definition - they will not be overridden
- Forms should inherit from `BaseModelForm` and use `BaseModelFormMeta` as the Meta parent class

Example form structure:
```python
from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from django.forms import DateInput

class MyModelForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = MyModel
        widgets = {
            'date_field': DateInput(attrs={'type': 'date'}),  # Classes added automatically
        }
```

### GitLab Integration

The GitLab integration uses the `python-gitlab` library to fetch data from a GitLab instance. Key points:

- API modules in `git_lab/apis/` make requests to GitLab and sync to local database models
- `core.utilities.git_lab.get_git_lab_client()` provides the configured GitLab client
- Configuration is stored in `ThisServerConfiguration` model (connection URL, API token, top-level group ID)
- All GitLab timestamps are converted to UTC using `convert_and_enforce_utc_timezone()`
- GitLab entities use the GitLab ID as the primary key (via `AbstractGitLabPrimaryKey`)

### URL Structure

URLs are organized with an authenticated wrapper:
- `/` - Login/home (unauthenticated)
- `/authenticated/` - All authenticated routes under this prefix
- `/authenticated/admin/` - Django admin
- `/authenticated/kpi/` - KPI namespace
- `/authenticated/api/` - API endpoints

URL patterns are split into modular files under `core/urls/` (e.g., `urlpatterns_application.py`, `urlpatterns_person.py`)

### Utilities

Core utilities in `core/utilities/`:
- `encryption.py` - Encrypt/decrypt sensitive data
- `cast_query_set.py` - Type-safe QuerySet casting
- `get_user_from_request.py` - Extract user from request
- `safe_divide.py` - Division with zero handling
- `coerce_integer.py` / `coerce_float.py` - Type coercion
- `get_name_acronym.py` - Format name/acronym display
- `wrap_with_global_context.py` - Add global context to views
- `git_lab/` subdirectory - GitLab-specific utilities

### Authentication

The application supports two authentication backends:
1. Django's built-in authentication (default)
2. LDAP authentication via `django-auth-ldap` (when `SHOULD_USE_LDAP=True`)

All views require login via `@login_required` decorator or URL-level wrapping.

## Key Dependencies

**Python/Django:**
- **Django 5.1.7** - Web framework
- **python-gitlab 5.6.0** - GitLab API client
- **django-simple-history 3.8.0** - Model history tracking
- **django-auth-ldap 5.1.0** - LDAP authentication
- **django-generic-model-fields 2.0.0** - Generic model field helpers
- **django-environ 0.12.0** - Environment variable management
- **django-hijack 3.7.1** - User impersonation for admin
- **django-storages[s3]** - MinIO/S3 storage backend
- **boto3** - AWS SDK for MinIO integration
- **humanize 4.12.1** - Human-readable formatting

**Node.js:**
- **Tailwind CSS** - Utility-first CSS framework

**Infrastructure (Docker):**
- **MinIO** - S3-compatible object storage
- **nginx** - Reverse proxy with SSL termination

## Additional Documentation

More detailed documentation is available in the `.documentation/` directory:
- `environment-setup.md` - Environment setup details
- `commands-python-unix.md` - UNIX-specific Python commands
- `commands-python-windows.md` - Windows-specific Python commands

## External Resources

- [python-gitlab documentation](https://python-gitlab.readthedocs.io/en/stable/api/gitlab.v4.html) - Official API docs for the GitLab library
