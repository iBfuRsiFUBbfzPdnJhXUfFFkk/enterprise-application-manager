"""
Tests for WebAuthn utility functions.

These utilities support multi-hostname passkey authentication by dynamically
determining the RP_ID and origin from the request hostname.
"""
from django.test import TestCase, RequestFactory

from core.utilities.webauthn import get_webauthn_rp_id, get_webauthn_origin


class TestWebAuthnUtils(TestCase):
    """Unit tests for WebAuthn utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_get_webauthn_rp_id_localhost(self):
        """Verify RP_ID extraction for localhost."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = 'localhost:50478'
        self.assertEqual(get_webauthn_rp_id(request), 'localhost')

    def test_get_webauthn_rp_id_localhost_no_port(self):
        """Verify RP_ID extraction for localhost without port."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = 'localhost'
        self.assertEqual(get_webauthn_rp_id(request), 'localhost')

    def test_get_webauthn_rp_id_hostname_local(self):
        """Verify RP_ID extraction for hostname.local (mDNS)."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = 'my-macbook.local:50478'
        self.assertEqual(get_webauthn_rp_id(request), 'my-macbook.local')

    def test_get_webauthn_rp_id_hostname_dev(self):
        """Verify RP_ID extraction for hostname.dev."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = 'my-macbook.dev:50478'
        self.assertEqual(get_webauthn_rp_id(request), 'my-macbook.dev')

    def test_get_webauthn_rp_id_hostname_test(self):
        """Verify RP_ID extraction for hostname.test."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = 'my-macbook.test:50478'
        self.assertEqual(get_webauthn_rp_id(request), 'my-macbook.test')

    def test_get_webauthn_rp_id_ip_address(self):
        """Verify RP_ID extraction for IP address."""
        request = self.factory.get('/')
        request.META['HTTP_HOST'] = '127.0.0.1:50478'
        self.assertEqual(get_webauthn_rp_id(request), '127.0.0.1')

    def test_get_webauthn_origin_https(self):
        """Verify origin construction for HTTPS."""
        request = self.factory.get('/', secure=True)
        request.META['HTTP_HOST'] = 'localhost:50478'
        self.assertEqual(get_webauthn_origin(request), 'https://localhost:50478')

    def test_get_webauthn_origin_http(self):
        """Verify origin construction for HTTP."""
        request = self.factory.get('/', secure=False)
        request.META['HTTP_HOST'] = 'localhost:8000'
        self.assertEqual(get_webauthn_origin(request), 'http://localhost:8000')

    def test_get_webauthn_origin_hostname_local(self):
        """Verify origin construction for hostname.local."""
        request = self.factory.get('/', secure=True)
        request.META['HTTP_HOST'] = 'my-macbook.local:50478'
        self.assertEqual(get_webauthn_origin(request), 'https://my-macbook.local:50478')

    def test_get_webauthn_origin_no_port(self):
        """Verify origin construction without port."""
        request = self.factory.get('/', secure=True)
        request.META['HTTP_HOST'] = 'localhost'
        self.assertEqual(get_webauthn_origin(request), 'https://localhost')

    def test_rp_id_and_origin_consistency(self):
        """Verify RP_ID is a suffix of the origin hostname."""
        test_cases = [
            ('localhost:50478', True),
            ('my-macbook.local:50478', True),
            ('my-macbook.dev:50478', True),
            ('127.0.0.1:50478', True),
        ]

        for host, secure in test_cases:
            request = self.factory.get('/', secure=secure)
            request.META['HTTP_HOST'] = host

            rp_id = get_webauthn_rp_id(request)
            origin = get_webauthn_origin(request)

            # RP_ID should be the hostname part of the origin
            expected_hostname = host.split(':')[0] if ':' in host else host
            self.assertEqual(rp_id, expected_hostname, f"RP_ID mismatch for {host}")
            self.assertIn(rp_id, origin, f"RP_ID should be in origin for {host}")
