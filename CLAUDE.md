# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Enterprise Application Manager is a Django-based web application designed to help organizations manage large amounts of custom applications. It integrates with GitLab to track projects, issues, merge requests, and provides Scrum/Agile management capabilities along with KPI tracking.

## Development Environment Setup

### Virtual Environment

Activate the Python virtual environment:
```bash
bash .venv/bin/activate
```

Deactivate when done:
```bash
deactivate
```

### Environment Configuration

Set the Django settings environment before running commands:
```bash
export DJANGO_SETTINGS_MODULE="core.settings.local"
```

Available settings modules:
- `core.settings.local` - Local development
- `core.settings.development` - Development environment
- `core.settings.staging` - Staging environment
- `core.settings.production` - Production environment

### Required Environment Variables

Create a `.env` file in the root directory with these variables (see `.documentation/environment-setup.md` for details):
- `DJANGO_SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - JSON array of allowed hosts
- `ENCRYPTION_SECRET` - Encryption key for sensitive data
- `SHOULD_USE_LDAP` - Enable LDAP authentication (True/False)
- LDAP configuration (`AUTH_LDAP_*` variables) if using LDAP
- Email configuration (`EMAIL_*` variables)

## Common Commands

### Running the Development Server

```bash
.venv/bin/python manage.py runserver
```

### Database Operations

Run migrations:
```bash
.venv/bin/python manage.py migrate
```

Create new migrations:
```bash
.venv/bin/python manage.py makemigrations
```

Dump database to JSON:
```bash
.venv/bin/python manage.py dumpdata --indent=2 > data.json
```

Load database from JSON:
```bash
.venv/bin/python manage.py loaddata data.json
```

### Package Management

Freeze requirements:
```bash
.venv/bin/python -m pip freeze > requirements.txt
```

Install requirements:
```bash
.venv/bin/python -m pip install -r requirements.txt
```

### Testing

Run a specific test:
```bash
.venv/bin/python manage.py test <app_name>.tests.<test_file>.<TestClass>.<test_method>
```

Run all tests for an app:
```bash
.venv/bin/python manage.py test <app_name>
```

## Architecture

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

- **Django 5.1.7** - Web framework
- **python-gitlab 5.6.0** - GitLab API client
- **django-simple-history 3.8.0** - Model history tracking
- **django-auth-ldap 5.1.0** - LDAP authentication
- **django-generic-model-fields 2.0.0** - Generic model field helpers
- **django-environ 0.12.0** - Environment variable management
- **django-hijack 3.7.1** - User impersonation for admin
- **humanize 4.12.1** - Human-readable formatting

## Additional Documentation

More detailed documentation is available in the `.documentation/` directory:
- `environment-setup.md` - Environment setup details
- `commands-python-unix.md` - UNIX-specific Python commands
- `commands-python-windows.md` - Windows-specific Python commands

## External Resources

- [python-gitlab documentation](https://python-gitlab.readthedocs.io/en/stable/api/gitlab.v4.html) - Official API docs for the GitLab library
