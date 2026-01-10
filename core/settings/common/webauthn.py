from core.settings.common.environment import env

# WebAuthn / Passkey Configuration

# Relying Party (RP) Name - displayed to users during passkey registration
WEBAUTHN_RP_NAME: str = env(var='WEBAUTHN_RP_NAME', default='Enterprise Application Manager')

# Relying Party ID - must match the domain (without port)
# For localhost development: 'localhost'
# For production: 'yourdomain.com'
WEBAUTHN_RP_ID: str = env(var='WEBAUTHN_RP_ID', default='localhost')

# Expected origin(s) for WebAuthn ceremonies
# For local development: http://localhost:8000 or https://localhost
# For production: https://yourdomain.com
WEBAUTHN_ORIGIN: str = env(var='WEBAUTHN_ORIGIN', default='http://localhost:8000')

# Challenge timeout (in milliseconds) - default 5 minutes
WEBAUTHN_CHALLENGE_TIMEOUT_MS: int = 300000  # 5 minutes

# User verification requirement
# Options: 'required', 'preferred', 'discouraged'
# 'required' = always require biometrics/PIN
# 'preferred' = use biometrics/PIN if available
# 'discouraged' = don't require user verification
WEBAUTHN_USER_VERIFICATION: str = 'preferred'

# Authenticator attachment
# Options: 'platform', 'cross-platform', None
# 'platform' = built-in authenticators only (Face ID, Touch ID, Windows Hello)
# 'cross-platform' = external authenticators only (security keys)
# None = allow both
WEBAUTHN_AUTHENTICATOR_ATTACHMENT: str | None = None  # Allow both platform and cross-platform

# Attestation conveyance
# Options: 'none', 'indirect', 'direct', 'enterprise'
# 'none' = no attestation (recommended for most use cases)
WEBAUTHN_ATTESTATION: str = 'none'

# Resident key requirement
# Options: 'required', 'preferred', 'discouraged'
# 'required' = require resident keys (enables passwordless)
# 'preferred' = use resident keys if available
WEBAUTHN_RESIDENT_KEY: str = 'preferred'

# Feature flags
WEBAUTHN_ENABLED: bool = env(var='WEBAUTHN_ENABLED', default=True, cast=bool)
