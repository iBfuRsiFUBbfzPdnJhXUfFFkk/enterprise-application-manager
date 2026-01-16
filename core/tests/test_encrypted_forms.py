"""
Tests for encrypted field forms to verify proper handling of encrypted data.

This test suite ensures that forms with encrypted fields:
1. Display blank fields when editing (not encrypted strings)
2. Preserve existing encrypted values when fields are left blank
3. Properly encrypt new values when provided
4. Don't corrupt data through multiple edit cycles
"""
from django.test import TestCase

from core.forms.database_form import DatabaseForm
from core.forms.login_credential_form import LoginCredentialForm
from core.forms.secret_form import SecretForm
from core.models.database import Database
from core.models.login_credential import LoginCredential
from core.models.secret import Secret
from core.utilities.encryption import decrypt_secret, encrypt_secret


class TestEncryptedFieldForms(TestCase):
    """Unit tests for encrypted field forms."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_password = "test_password_123"
        self.test_username = "test_user"
        self.test_secret_value = "secret_value_456"

    def test_database_form_edit_clears_encrypted_fields(self):
        """Verify DatabaseForm clears encrypted fields when editing."""
        # Create a database with encrypted fields
        database = Database.objects.create(
            encrypted_password=encrypt_secret(self.test_password),
            encrypted_username=encrypt_secret(self.test_username),
        )

        # Create form in edit mode
        form = DatabaseForm(instance=database)

        # Verify encrypted fields are cleared
        self.assertIsNone(form.fields['encrypted_password'].initial)
        self.assertIsNone(form.fields['encrypted_username'].initial)

        # Verify placeholder text is set
        self.assertEqual(
            form.fields['encrypted_password'].widget.attrs['placeholder'],
            'Leave blank to keep existing value'
        )
        self.assertEqual(
            form.fields['encrypted_username'].widget.attrs['placeholder'],
            'Leave blank to keep existing value'
        )

    def test_database_form_edit_preserves_blank_fields(self):
        """Verify leaving encrypted fields blank preserves existing values."""
        # Create a database with encrypted fields
        database = Database.objects.create(
            encrypted_password=encrypt_secret(self.test_password),
            encrypted_username=encrypt_secret(self.test_username),
        )

        # Store original encrypted values
        original_password = database.encrypted_password
        original_username = database.encrypted_username

        # Create form with blank encrypted fields (simulating edit without changes)
        form = DatabaseForm(
            data={
                'encrypted_password': '',
                'encrypted_username': '',
            },
            instance=database
        )

        # Save the form
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        saved_database = form.save()

        # Verify encrypted values are preserved
        self.assertEqual(saved_database.encrypted_password, original_password)
        self.assertEqual(saved_database.encrypted_username, original_username)

        # Verify we can still decrypt the values
        self.assertEqual(decrypt_secret(saved_database.encrypted_password), self.test_password)
        self.assertEqual(decrypt_secret(saved_database.encrypted_username), self.test_username)

    def test_database_form_edit_updates_encrypted_fields(self):
        """Verify providing new values encrypts them properly."""
        # Create a database with encrypted fields
        database = Database.objects.create(
            encrypted_password=encrypt_secret(self.test_password),
            encrypted_username=encrypt_secret(self.test_username),
        )

        # Create form with new encrypted field values
        new_password = "new_password_789"
        new_username = "new_user"
        form = DatabaseForm(
            data={
                'encrypted_password': new_password,
                'encrypted_username': new_username,
            },
            instance=database
        )

        # Save the form
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        saved_database = form.save()

        # Verify new values are encrypted and saved
        self.assertNotEqual(saved_database.encrypted_password, new_password)
        self.assertNotEqual(saved_database.encrypted_username, new_username)

        # Verify we can decrypt the new values
        self.assertEqual(decrypt_secret(saved_database.encrypted_password), new_password)
        self.assertEqual(decrypt_secret(saved_database.encrypted_username), new_username)

    def test_database_form_multiple_edit_cycles_no_corruption(self):
        """Verify multiple edit cycles don't corrupt encrypted data."""
        # Create a database
        database = Database.objects.create(
            encrypted_password=encrypt_secret(self.test_password),
        )

        # First edit: leave password blank
        form1 = DatabaseForm(
            data={'encrypted_password': ''},
            instance=database
        )
        self.assertTrue(form1.is_valid())
        database = form1.save()
        first_edit_password = database.encrypted_password

        # Second edit: leave password blank again
        form2 = DatabaseForm(
            data={'encrypted_password': ''},
            instance=database
        )
        self.assertTrue(form2.is_valid())
        database = form2.save()
        second_edit_password = database.encrypted_password

        # Third edit: change password
        new_password = "completely_new_password"
        form3 = DatabaseForm(
            data={'encrypted_password': new_password},
            instance=database
        )
        self.assertTrue(form3.is_valid())
        database = form3.save()

        # Verify password is still correct after all edits
        self.assertEqual(decrypt_secret(database.encrypted_password), new_password)

        # Verify previous blank edits preserved the original
        self.assertEqual(first_edit_password, second_edit_password)

    def test_login_credential_form_edit_clears_encrypted_fields(self):
        """Verify LoginCredentialForm clears encrypted fields when editing."""
        # Create a login credential with encrypted password
        credential = LoginCredential.objects.create(
            name="Test Credential",
            encrypted_password=encrypt_secret(self.test_password),
        )

        # Create form in edit mode
        form = LoginCredentialForm(instance=credential)

        # Verify encrypted field is cleared
        self.assertIsNone(form.fields['encrypted_password'].initial)

        # Verify placeholder text is set
        self.assertEqual(
            form.fields['encrypted_password'].widget.attrs['placeholder'],
            'Leave blank to keep existing value'
        )

    def test_secret_form_edit_clears_encrypted_fields(self):
        """Verify SecretForm clears encrypted fields when editing."""
        # Create a secret with encrypted value
        secret = Secret.objects.create(
            name="Test Secret",
            encrypted_value=encrypt_secret(self.test_secret_value),
        )

        # Create form in edit mode
        form = SecretForm(instance=secret)

        # Verify encrypted field is cleared
        self.assertIsNone(form.fields['encrypted_value'].initial)

        # Verify placeholder text is set
        self.assertEqual(
            form.fields['encrypted_value'].widget.attrs['placeholder'],
            'Leave blank to keep existing value'
        )

    def test_create_mode_allows_initial_values(self):
        """Verify create mode (no instance) is unaffected by the mixin."""
        # Create form without instance (create mode)
        form = DatabaseForm()

        # Verify fields don't have placeholder text in create mode
        self.assertNotIn('placeholder', form.fields['encrypted_password'].widget.attrs)

    def test_encrypted_field_widget_placeholder(self):
        """Verify encrypted fields have correct placeholder text."""
        # Create a database for editing
        database = Database.objects.create(
            encrypted_password=encrypt_secret(self.test_password),
        )

        # Create form in edit mode
        form = DatabaseForm(instance=database)

        # Check all encrypted fields have the correct placeholder
        encrypted_fields = [
            'encrypted_password',
            'encrypted_username',
            'encrypted_ssh_tunnel_username',
            'encrypted_ssh_tunnel_password',
        ]

        for field_name in encrypted_fields:
            self.assertEqual(
                form.fields[field_name].widget.attrs.get('placeholder'),
                'Leave blank to keep existing value',
                f"Field {field_name} should have placeholder text"
            )


