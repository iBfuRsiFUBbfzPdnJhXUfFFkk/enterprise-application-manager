/**
 * Passkey Management Operations
 * Handles rename and delete operations for passkeys
 */

(function() {
    'use strict';

    // Get CSRF token for Django
    function getCSRFToken() {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('eam_csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    // Rename passkey
    window.renamePasskey = async function(passkeyUuid) {
        const currentName = document.getElementById(`passkey-name-${passkeyUuid}`).textContent.trim();
        const newName = prompt('Enter new name for this passkey:', currentName);

        if (!newName || newName === currentName) return;

        try {
            const response = await fetch(`/authenticated/passkey/rename/${passkeyUuid}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ name: newName }),
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById(`passkey-name-${passkeyUuid}`).textContent = newName;
                alert('Passkey renamed successfully!');
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error renaming passkey:', error);
            alert('Failed to rename passkey: ' + error.message);
        }
    };

    // Delete passkey
    window.deletePasskey = async function(passkeyUuid) {
        if (!confirm('Are you sure you want to delete this passkey? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`/authenticated/passkey/delete/${passkeyUuid}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
            });

            const result = await response.json();

            if (result.success) {
                alert('Passkey deleted successfully!');
                location.reload();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error deleting passkey:', error);
            alert('Failed to delete passkey: ' + error.message);
        }
    };
})();
