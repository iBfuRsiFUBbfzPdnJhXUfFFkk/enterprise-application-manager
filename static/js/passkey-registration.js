/**
 * Passkey Registration Flow
 * Handles adding new passkeys for authenticated users
 */

(function() {
    'use strict';

    const addPasskeyButton = document.getElementById('addPasskeyButton');
    if (!addPasskeyButton) return;

    // Check WebAuthn support
    if (!window.PublicKeyCredential) {
        addPasskeyButton.disabled = true;
        addPasskeyButton.textContent = 'Passkeys not supported in this browser';
        return;
    }

    addPasskeyButton.addEventListener('click', async function() {
        try {
            // Prompt for passkey name
            const passkeyName = prompt('Enter a name for this passkey (e.g., "iPhone 15", "Windows Hello"):');
            if (!passkeyName) return;

            addPasskeyButton.disabled = true;
            addPasskeyButton.innerHTML = '<span class="inline-block animate-spin mr-2">⏳</span> Registering...';

            // Step 1: Get registration options from server
            const beginResponse = await fetch('/authenticated/passkey/register/begin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ name: passkeyName }),
            });

            if (!beginResponse.ok) {
                throw new Error('Failed to begin registration');
            }

            const { options } = await beginResponse.json();

            // Convert base64url strings to ArrayBuffers
            const publicKeyCredentialCreationOptions = {
                ...options,
                challenge: base64urlToBuffer(options.challenge),
                user: {
                    ...options.user,
                    id: base64urlToBuffer(options.user.id),
                },
                excludeCredentials: options.excludeCredentials.map(cred => ({
                    ...cred,
                    id: base64urlToBuffer(cred.id),
                })),
            };

            // Step 2: Create credential
            const credential = await navigator.credentials.create({
                publicKey: publicKeyCredentialCreationOptions,
            });

            if (!credential) {
                throw new Error('No credential returned');
            }

            // Step 3: Send credential to server
            const completeResponse = await fetch('/authenticated/passkey/register/complete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    name: passkeyName,
                    id: credential.id,
                    rawId: bufferToBase64url(credential.rawId),
                    response: {
                        clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
                        attestationObject: bufferToBase64url(credential.response.attestationObject),
                    },
                    type: credential.type,
                }),
            });

            const result = await completeResponse.json();

            if (result.success) {
                alert('Passkey registered successfully!');
                location.reload();
            } else {
                throw new Error(result.error || 'Registration failed');
            }

        } catch (error) {
            console.error('Passkey registration error:', error);
            alert('Failed to register passkey: ' + error.message);
        } finally {
            addPasskeyButton.disabled = false;
            addPasskeyButton.innerHTML = `
                <svg class="w-5 h-5 mr-2 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Add New Passkey
            `;
        }
    });

    // Utility functions
    function getCSRFToken() {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('eam_csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    function base64urlToBuffer(base64url) {
        const base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
        const padLen = (4 - (base64.length % 4)) % 4;
        const padded = base64 + '='.repeat(padLen);
        const binary = atob(padded);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes.buffer;
    }

    function bufferToBase64url(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = '';
        for (let i = 0; i < bytes.length; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        const base64 = btoa(binary);
        return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    }
})();
