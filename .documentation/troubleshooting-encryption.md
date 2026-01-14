# Encryption Troubleshooting Guide

This guide helps you diagnose and fix encryption-related issues in the Enterprise Application Manager.

## Table of Contents

- [Common Issues](#common-issues)
- [Diagnostic Commands](#diagnostic-commands)
- [Error Messages](#error-messages)
- [Recovery Procedures](#recovery-procedures)
- [Prevention](#prevention)

## Common Issues

### Issue 1: Wrong ENCRYPTION_SECRET

**Symptoms:**
- `InvalidEncryptionKeyError` when viewing records
- Health check endpoint returns `"encryption_key": "invalid"`
- Logs show "Decryption failed" errors
- Cannot view passwords or secrets

**Cause:**
The `ENCRYPTION_SECRET` environment variable doesn't match the key used to encrypt the data.

**Solution:**

1. **Check current ENCRYPTION_SECRET:**
   ```bash
   docker compose exec web printenv ENCRYPTION_SECRET
   ```

2. **Verify it matches your `.env` file:**
   ```bash
   cat .env | grep ENCRYPTION_SECRET
   ```

3. **If they don't match, restart the container:**
   ```bash
   docker compose restart web
   ```

4. **Validate after restart:**
   ```bash
   docker compose exec web python manage.py validate_encrypted_data
   ```

5. **If still failing, you may have changed the key**:
   - Restore the old key from backup
   - Or restore database from backup

**Prevention:**
- Never change `ENCRYPTION_SECRET` without following the key rotation procedure
- Keep encrypted backups of the original key
- Document key changes in your deployment log

---

### Issue 2: Encrypted Values Overwritten with Blank

**Symptoms:**
- Passwords stop working after editing a record
- Encrypted fields become None/empty
- User reports "I didn't change the password but now it doesn't work"

**Cause:**
This was a bug in versions before the encryption fix. Leaving encrypted fields blank during edit overwrote existing values.

**Status:**
✅ **FIXED** - The blank field overwrite bug has been fixed. Blank fields now preserve existing encrypted values.

**Solution:**
If you have corrupted data from before the fix:

1. **Check if you have a database backup:**
   ```bash
   ls -lt backup*.json | head -5
   ```

2. **Restore the specific record from backup** (if available)

3. **If no backup, manually re-enter the password:**
   - Navigate to the record's edit form
   - Enter the correct password
   - Save

**Verification:**
Test the fix is working:
1. Edit a Database record
2. Leave the password field blank
3. Save
4. Check the connection still works with the original password

---

### Issue 3: Legacy Format Warning

**Symptoms:**
- `validate_encrypted_data` shows "legacy_format" count > 0
- Health check shows warnings about legacy format
- Logs show "Decrypted legacy format" warnings

**Cause:**
Data was encrypted before the v1 format upgrade. This is normal and not an error.

**Impact:**
- Low - Legacy data still works correctly
- No functionality is lost
- Security is not compromised

**Solution (Optional):**

Upgrade legacy format to v1:

```bash
# Dry run first to see what will change
docker compose exec web python manage.py validate_encrypted_data --dry-run --fix

# Actual upgrade
docker compose exec web python manage.py validate_encrypted_data --fix
```

**After upgrade:**
```bash
# Verify all converted to v1
docker compose exec web python manage.py validate_encrypted_data
```

**Why upgrade?**
- Enhanced integrity validation
- Better error detection
- Future-proof format

---

### Issue 4: Application Won't Start - ENCRYPTION_SECRET Missing

**Symptoms:**
- Container crashes on startup
- Error: "ENCRYPTION_SECRET environment variable not set"
- Application logs show ValueError

**Cause:**
`ENCRYPTION_SECRET` is not set in `.env` file.

**Solution:**

1. **Check if .env exists:**
   ```bash
   ls -la .env
   ```

2. **Check if ENCRYPTION_SECRET is set:**
   ```bash
   cat .env | grep ENCRYPTION_SECRET
   ```

3. **If missing, generate a new key:**
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

4. **Add to .env file:**
   ```bash
   echo "ENCRYPTION_SECRET=<generated_key>" >> .env
   ```

5. **Restart:**
   ```bash
   docker compose up
   ```

**⚠️ WARNING:**
If you generate a new key, you won't be able to decrypt existing data! Only do this for:
- Fresh installations
- After data migration with re-encryption
- Emergency recovery (will lose existing encrypted data)

---

### Issue 5: Health Check Endpoint Returns 500 Error

**Symptoms:**
- `/authenticated/health/encryption/` returns HTTP 500
- JSON response shows `"status": "error"`
- Logs show exceptions in health check

**Diagnosis:**

1. **Check health check logs:**
   ```bash
   docker compose exec web python manage.py shell
   >>> from core.utilities.encryption_health_check import get_encryption_status
   >>> get_encryption_status()
   ```

2. **Check encryption logs:**
   ```bash
   docker compose exec web tail -20 logs/encryption.log
   ```

**Common Causes:**
- Wrong ENCRYPTION_SECRET (most common)
- Corrupted database data
- Missing logs directory
- Permission issues

**Solution:**
1. Fix the underlying issue (usually wrong key)
2. Restart application
3. Re-check health endpoint

---

### Issue 6: CharField Max Length Exceeded

**Symptoms:**
- Error: "Data too long for column 'encrypted_password'"
- Very long passwords fail to save
- Form validation error on save

**Cause:**
Encrypted data exceeds CharField(max_length=255).

Fernet encryption adds overhead:
- ~44 bytes base overhead
- v1 format adds ~15 bytes (`v1:abcd1234:`)
- Total overhead: ~59 bytes

**Solution:**

For very long passwords (>196 characters), you may need to increase field length:

1. **Create migration to increase field length:**
   ```python
   # In a new migration file
   operations = [
       migrations.AlterField(
           model_name='secret',
           name='encrypted_value',
           field=models.CharField(max_length=512, null=True, blank=True),
       ),
   ]
   ```

2. **Run migration:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

**Prevention:**
- Most passwords are <100 characters, so this is rare
- Consider password policies limiting length
- Current limit supports passwords up to ~196 characters

---

## Diagnostic Commands

### Quick Health Check
```bash
# Via management script (interactive)
./manage.sh
# Select: 8) Django commands → 8) Validate encrypted data

# Via direct command
docker compose exec web python manage.py validate_encrypted_data
```

### Detailed Validation with Verbose Output
```bash
docker compose exec web python manage.py validate_encrypted_data --verbose
```

### Check Health Endpoint (requires authentication)
```bash
curl -u username:password https://localhost:50478/authenticated/health/encryption/ | jq
```

### View Encryption Logs
```bash
# Last 50 lines
docker compose exec web tail -50 logs/encryption.log

# Watch in real-time
docker compose exec web tail -f logs/encryption.log

# Search for errors
docker compose exec web grep ERROR logs/encryption.log

# Search for specific record
docker compose exec web grep "Database id=42" logs/encryption.log
```

### Test Encryption/Decryption in Shell
```bash
docker compose exec web python manage.py shell
```
```python
from core.utilities.encryption import encrypt_secret, decrypt_secret

# Test encryption
encrypted = encrypt_secret("test_password_123")
print(f"Encrypted: {encrypted}")
print(f"Format: {'v1' if encrypted.startswith('v1:') else 'legacy'}")

# Test decryption
decrypted = decrypt_secret(encrypted)
print(f"Decrypted: {decrypted}")
print(f"Match: {decrypted == 'test_password_123'}")
```

### Check Specific Record
```bash
docker compose exec web python manage.py shell
```
```python
from core.models.secret import Secret
from core.utilities.encryption import detect_encryption_format

secret = Secret.objects.get(id=5)
print(f"Encrypted value: {secret.encrypted_value[:50]}...")
print(f"Format: {detect_encryption_format(secret.encrypted_value)}")

# Try to decrypt
try:
    decrypted = secret.get_encrypted_value()
    print(f"Decryption: SUCCESS (length={len(decrypted)})")
except Exception as e:
    print(f"Decryption: FAILED - {e}")
```

### Count Encrypted Fields
```bash
docker compose exec web python manage.py shell
```
```python
from django.db.models import Q
from core.models.secret import Secret
from core.models.login_credential import LoginCredential
from core.models.database import Database

# Count by model
secrets = Secret.objects.exclude(Q(encrypted_value__isnull=True) | Q(encrypted_value='')).count()
credentials = LoginCredential.objects.exclude(Q(encrypted_password__isnull=True) | Q(encrypted_password='')).count()

# Count Database fields
db_count = 0
for db in Database.objects.all():
    if db.encrypted_password: db_count += 1
    if db.encrypted_username: db_count += 1
    if db.encrypted_ssh_tunnel_username: db_count += 1
    if db.encrypted_ssh_tunnel_password: db_count += 1

print(f"Secrets: {secrets}")
print(f"LoginCredentials: {credentials}")
print(f"Database fields: {db_count}")
print(f"Total: {secrets + credentials + db_count}")
```

## Error Messages

### `InvalidEncryptionKeyError: Failed to decrypt data`

**Meaning:** The ENCRYPTION_SECRET is incorrect or data is corrupted.

**Check:**
1. Verify ENCRYPTION_SECRET matches original key
2. Check if key was recently changed
3. Verify data wasn't manually edited in database

**Fix:**
- Restore correct ENCRYPTION_SECRET from backup
- Or restore database from backup

---

### `CorruptedDataError: Encrypted data format is invalid`

**Meaning:** The encrypted data string is malformed.

**Causes:**
- Database corruption
- Manual editing of encrypted field
- Character encoding issues
- Truncated data

**Fix:**
- Restore record from backup
- Or manually re-enter the secret value

---

### `DecryptionFailureError: Unexpected error during decryption`

**Meaning:** An unexpected error occurred during decryption.

**Check logs:**
```bash
docker compose exec web grep "Unexpected decryption error" logs/encryption.log
```

**Fix:**
- Review log details
- Check database integrity
- Verify Python dependencies installed correctly

---

### `Preserving existing encrypted value - form field was blank`

**Meaning:** (INFO level) This is working correctly! A blank field preserved the existing value.

**Action:** None required. This is the expected behavior after the blank field fix.

---

## Recovery Procedures

### Procedure 1: Restore from Database Backup

If you have a database backup with correct encryption:

```bash
# Stop application
docker compose down

# Restore database
docker compose up -d
docker compose exec web python manage.py loaddata backup.json

# Verify
docker compose exec web python manage.py validate_encrypted_data
```

### Procedure 2: Selective Record Restoration

If only some records are corrupted:

1. **Export good data from backup:**
   ```bash
   docker compose exec web python manage.py shell
   ```
   ```python
   from core.models.secret import Secret
   import json

   # Find the corrupted record ID
   corrupted_id = 5

   # From backup JSON, extract that record's data
   # Then manually re-create or update
   ```

2. **Manually re-enter the value:**
   - Navigate to the record's edit form in web UI
   - Enter the correct password/secret
   - Save (will re-encrypt with current key)

### Procedure 3: Emergency Key Reset (DATA LOSS)

⚠️ **WARNING:** This will make all existing encrypted data unrecoverable!

Only use if:
- No backup available
- Data is already corrupted beyond recovery
- Fresh installation

```bash
# Generate new key
NEW_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Update .env
sed -i.bak "s/ENCRYPTION_SECRET=.*/ENCRYPTION_SECRET=$NEW_KEY/" .env

# Restart
docker compose restart web

# Delete all encrypted data (will need to be re-entered)
docker compose exec web python manage.py shell
```
```python
from core.models.secret import Secret
from core.models.login_credential import LoginCredential
from core.models.database import Database

# Clear all encrypted fields
Secret.objects.all().update(encrypted_value=None)
LoginCredential.objects.all().update(encrypted_password=None)
Database.objects.all().update(
    encrypted_password=None,
    encrypted_username=None,
    encrypted_ssh_tunnel_username=None,
    encrypted_ssh_tunnel_password=None
)
```

## Prevention

### 1. Regular Backups

```bash
# Automated backup script
docker compose exec web python manage.py dumpdata > "backup-$(date +%Y%m%d-%H%M%S).json"
```

### 2. Document ENCRYPTION_SECRET

Store ENCRYPTION_SECRET securely:
- In password manager
- In encrypted backup
- In deployment documentation

Never:
- Commit to git
- Store in plaintext
- Share via insecure channels

### 3. Monitor Health Check

Add to uptime monitoring:
```bash
# Check every 5 minutes
*/5 * * * * curl -f https://localhost:50478/authenticated/health/encryption/ || alert
```

### 4. Review Logs Regularly

```bash
# Weekly check for errors
docker compose exec web grep ERROR logs/encryption.log | tail -20
```

### 5. Test Before Production

Before deploying:
1. Test in staging environment
2. Validate encryption works: `validate_encrypted_data`
3. Check health endpoint
4. Review logs for warnings

### 6. User Training

Educate users:
- Leave password fields blank when not changing them
- Don't edit encrypted data directly in database
- Report "password stopped working" immediately

## Getting Help

If issues persist:

1. **Gather diagnostic information:**
   ```bash
   docker compose exec web python manage.py validate_encrypted_data --verbose > diagnostic.txt
   docker compose exec web cat logs/encryption.log > encryption-log.txt
   ```

2. **Check documentation:**
   - [encryption-architecture.md](encryption-architecture.md) - System architecture
   - [CLAUDE.md](../CLAUDE.md) - Project documentation

3. **Review code:**
   - `core/utilities/encryption.py` - Encryption implementation
   - `core/forms/common/generic_encrypted_save.py` - Form handling
   - `core/management/commands/validate_encrypted_data.py` - Validation logic
