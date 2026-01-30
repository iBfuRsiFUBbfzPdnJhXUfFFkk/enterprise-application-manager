"""
WebAuthn utility functions for multi-hostname passkey support.

WebAuthn RP_ID Limitation: The WebAuthn spec requires the RP_ID to be a domain
suffix of the origin. A passkey registered on `localhost` will NOT work on
`hostname.local` - this is by design.

| Origin                          | Valid RP_ID       |
|---------------------------------|-------------------|
| https://localhost:50478         | localhost         |
| https://hostname.local:50478    | hostname.local    |
| https://hostname.dev:50478      | hostname.dev      |
| https://127.0.0.1:50478         | 127.0.0.1         |
"""

from django.http import HttpRequest


def get_webauthn_rp_id(request: HttpRequest) -> str:
    """
    Extract hostname (without port) as the WebAuthn RP_ID.

    The RP_ID must match the domain of the origin where the passkey ceremony
    is being performed. This enables multi-hostname passkey support.
    """
    host = request.get_host()
    return host.split(':')[0] if ':' in host else host


def get_webauthn_origin(request: HttpRequest) -> str:
    """
    Construct the WebAuthn origin (scheme + host with port).

    The origin must exactly match what the browser sends during WebAuthn
    ceremonies. This includes the protocol (http/https) and port if non-standard.
    """
    scheme = 'https' if request.is_secure() else 'http'
    return f"{scheme}://{request.get_host()}"
