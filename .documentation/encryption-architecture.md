# Encryption Architecture

This document describes the encryption system architecture used in the Enterprise Application Manager.

## Overview

The application uses **Fernet symmetric encryption** (from the `cryptography` library) to protect sensitive data such as passwords, API keys, and secrets. The encryption system has been enhanced with validation, integrity checking, and comprehensive monitoring.

## Table of Contents

- [Encryption Format](#encryption-format)
- [Architecture Components](#architecture-components)
- [Data Flow](#data-flow)
- [Security Features](#security-features)
- [Key Rotation](#key-rotation)
- [Monitoring](#monitoring)

## Encryption Format

### v1 Format (Current)

The current encryption format includes integrity validation using SHA256 checksums:

```
v1:{sha256_hash[:8]}:{fernet_encrypted_data}
```

**Example:**
```
v1:a1b2c3d4:gAAAAABh5K8L9m2Q...base64_encrypted_data...
```

**Components:**
- `v1` - Version identifier for future compatibility
- `a1b2c3d4` - First 8 characters of SHA256 hash of the plaintext
- `gAAAAABh...` - Fernet-encrypted data (base64 encoded)

**Benefits:**
- **Integrity validation**: Hash mismatch indicates wrong encryption key or corrupted data
- **Versioning**: Allows future encryption format upgrades
- **Wrong key detection**: Immediately detects incorrect `ENCRYPTION_SECRET`

### Legacy Format (Backwards Compatible)

Data encrypted before the v1 format upgrade uses raw Fernet encryption:

```
gAAAAABh5K8L9m2Q...base64_encrypted_data...
```

**Migration Strategy:**
- Legacy format data is still readable (backwards compatible)
- New data is always encrypted in v1 format
- Lazy migration: legacy data upgrades to v1 on next save
- Force migration: Use `validate_encrypted_data --fix` command

## Architecture Components

### 1. Core Encryption Utility (`core/utilities/encryption.py`)

**Main Functions:**
- `encrypt_secret(secret: str | None) -> str | None`
  - Encrypts plaintext using Fernet
  - Adds SHA256 validation hash
  - Returns v1 formatted encrypted string

- `decrypt_secret(encrypted_secret: str | None) -> str | None`
  - Auto-detects format (v1 vs legacy)
  - Decrypts using Fernet
  - Validates hash for v1 format
  - Raises exceptions on validation failure

**Helper Functions:**
- `_compute_validation_hash()` - SHA256 hash computation
- `_format_encrypted_value()` - Adds v1 prefix
- `_parse_encrypted_value()` - Parses v1 format
- `detect_encryption_format()` - Detects v1 vs legacy
- `is_encrypted_value_valid()` - Format validation
- `validate_encrypted_data()` - Comprehensive validation

**Custom Exceptions:**
- `EncryptionError` - Base exception
- `DecryptionFailureError` - Generic decryption failure
- `InvalidEncryptionKeyError` - Wrong key or validation mismatch
- `CorruptedDataError` - Data format corruption

### 2. Model Layer

**Models with Encrypted Fields:**

#### Secret (`core/models/secret.py`)
- `encrypted_value` - CharField(max_length=255)
- `set_encrypted_value(secret)` - Setter method
- `get_encrypted_value()` - Getter method (decrypts)

#### LoginCredential (`core/models/login_credential.py`)
- `encrypted_password` - CharField(max_length=255)
- `set_encrypted_password(password)` - Setter method
- `get_decrypted_password()` - Getter method (decrypts)

#### Database (`core/models/database.py`)
- `encrypted_password` - CharField(max_length=255)
- `encrypted_username` - CharField(max_length=255)
- `encrypted_ssh_tunnel_username` - CharField(max_length=255)
- `encrypted_ssh_tunnel_password` - CharField(max_length=255)
- Getter/setter methods for each field

**Pattern:**
- Direct field access stores encrypted data
- Setter methods handle encryption automatically
- Getter methods handle decryption automatically
- Empty strings are treated as None (not encrypted)

### 3. Form Layer (`core/forms/common/generic_encrypted_save.py`)

The `generic_encrypted_save()` function handles encrypted field persistence:

```python
def generic_encrypted_save(model_form, instance, data_points):
    """
    Saves encrypted fields while preserving existing values when blank.

    Critical fix: Blank form fields preserve existing encrypted values
    instead of overwriting with empty/None.
    """
```

**Forms Using This:**
- `SecretForm` - Encrypts `encrypted_value`
- `LoginCredentialForm` - Encrypts `encrypted_password`
- `DatabaseForm` - Encrypts 4 password/username fields

### 4. Management Commands

#### `validate_encrypted_data`
```bash
python manage.py validate_encrypted_data [--verbose] [--fix]
```
- Scans all encrypted fields
- Validates encryption key is correct
- Reports v1 vs legacy format counts
- Can re-encrypt legacy format with `--fix`

#### `reencrypt_data`
```bash
python manage.py reencrypt_data [--force] [--dry-run]
```
- Re-encrypts all data (for key rotation)
- Confirmation prompt (unless `--force`)
- Dry-run mode available

### 5. Health Check System

#### Health Check Utility (`core/utilities/encryption_health_check.py`)
- `test_encryption_roundtrip()` - Tests encrypt/decrypt cycle
- `validate_encryption_key()` - Validates key correctness
- `scan_encrypted_data()` - Samples database for issues
- `get_encryption_status()` - Comprehensive status report

#### Health Check Endpoint (`/authenticated/health/encryption/`)
- Returns JSON status report
- Staff-only access
- HTTP 200 (healthy/warning) or 500 (error)

**Response Example:**
```json
{
  "status": "healthy",
  "encryption_key": "valid",
  "roundtrip_test": "passed",
  "database_sample": {
    "total_encrypted_fields": 245,
    "v1_format": 180,
    "legacy_format": 65,
    "failed_decryption": 0
  },
  "warnings": [],
  "timestamp": "2026-01-14T10:30:45Z"
}
```

### 6. Logging System (`core/settings/common/logging.py`)

**Log Files:**
- `logs/encryption.log` - Encryption-specific events (10MB, 5 backups)
- `logs/application.log` - General application logs (10MB, 10 backups)
- `logs/errors.log` - Error-level logs (10MB, 10 backups)

**Log Levels:**
- **DEBUG**: Successful encrypt/decrypt operations (dev only)
- **INFO**: Encryption operations, preserved values
- **WARNING**: Legacy format detected
- **ERROR**: Decryption failures, validation errors

## Data Flow

### Encryption Flow (Creating/Updating Records)

```
1. User submits form with sensitive data
   ↓
2. Form validation (cleaned_data)
   ↓
3. generic_encrypted_save() called
   ↓
4. Checks if field is blank
   ├─ If blank and existing value exists → PRESERVE (skip)
   └─ If not blank → Continue to step 5
   ↓
5. Model setter method (e.g., set_encrypted_password)
   ↓
6. encrypt_secret() function
   ├─ Encrypt with Fernet
   ├─ Compute SHA256 hash
   └─ Format as v1:{hash}:{encrypted}
   ↓
7. Save to database CharField
   ↓
8. Log encryption event
```

### Decryption Flow (Viewing/Using Records)

```
1. View/API accesses model instance
   ↓
2. Calls getter method (e.g., get_encrypted_password)
   ↓
3. decrypt_secret() function
   ↓
4. Detect format (v1 vs legacy)
   ↓
5a. If v1 format:
    ├─ Parse prefix (version, hash, encrypted_data)
    ├─ Decrypt with Fernet
    ├─ Compute SHA256 hash of plaintext
    ├─ Compare with stored hash
    │  ├─ Match → Return plaintext
    │  └─ Mismatch → Raise InvalidEncryptionKeyError
    └─ Log result

5b. If legacy format:
    ├─ Decrypt with Fernet
    ├─ Log warning about legacy format
    └─ Return plaintext
   ↓
6. Return plaintext to caller
```

## Security Features

### 1. Integrity Validation

Every v1 encrypted value includes a SHA256 hash of the plaintext. On decryption:
- Hash is recalculated from decrypted plaintext
- Compared with stored hash
- Mismatch = wrong key or corrupted data

### 2. Wrong Key Detection

If `ENCRYPTION_SECRET` is incorrect:
- v1 format: Immediate `InvalidEncryptionKeyError` raised
- Legacy format: `InvalidToken` caught and converted to error
- No silent failures (strict mode)

### 3. Blank Field Protection

Critical fix prevents accidental data loss:
- Editing a record with blank encrypted field preserves existing value
- Intentionally empty values (new records) save as None
- Logged for audit trail

### 4. Comprehensive Logging

All encryption events are logged:
- Successful encryptions/decryptions
- Legacy format warnings
- Validation failures
- Blank field preservation

### 5. Monitoring

Health check system provides:
- Real-time encryption status
- Sample-based validation
- Format distribution (v1 vs legacy)
- Early warning of issues

## Key Rotation

To rotate the `ENCRYPTION_SECRET`:

### Step 1: Backup Database
```bash
docker compose exec web python manage.py dumpdata > backup.json
```

### Step 2: Test Current Key
```bash
docker compose exec web python manage.py validate_encrypted_data
```
Ensure all fields decrypt successfully.

### Step 3: Update Environment Variable
Edit `.env`:
```bash
ENCRYPTION_SECRET=<new_base64_key>
```

### Step 4: Restart Application
```bash
docker compose restart web
```

### Step 5: Re-encrypt Data
```bash
# Dry run first
docker compose exec web python manage.py reencrypt_data --dry-run

# Actual re-encryption
docker compose exec web python manage.py reencrypt_data
```

### Step 6: Validate
```bash
docker compose exec web python manage.py validate_encrypted_data
```

## Monitoring

### Interactive Validation (via manage.sh)
```bash
./manage.sh
# Select: 8) Django commands → 8) Validate encrypted data
```

### Command Line Validation
```bash
docker compose exec web python manage.py validate_encrypted_data --verbose
```

### Health Check Endpoint
Access: `https://localhost:50478/authenticated/health/encryption/`

Requires staff authentication. Returns JSON status.

### Log Monitoring
```bash
# View encryption log
docker compose exec web cat logs/encryption.log

# Tail in real-time
docker compose exec web tail -f logs/encryption.log

# Search for errors
docker compose exec web grep ERROR logs/encryption.log
```

## Best Practices

1. **Never commit ENCRYPTION_SECRET to version control**
2. **Backup database before key rotation**
3. **Test decryption before changing keys**
4. **Monitor encryption logs regularly**
5. **Use health check endpoint in uptime monitoring**
6. **Validate after deployment**: Run `validate_encrypted_data` after deploying
7. **Keep logs directory writable**: Ensure `logs/` directory exists and is writable
8. **Use strong encryption keys**: Generate with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

## Troubleshooting

See [troubleshooting-encryption.md](troubleshooting-encryption.md) for detailed troubleshooting guidance.
