/**
 * Passkey Authentication Flow
 * Handles passwordless login using WebAuthn
 */

(function() {
    'use strict';

    const passkeyLoginButton = document.getElementById('passkeyLoginButton');
    if (!passkeyLoginButton) return;

    // Check WebAuthn support
    if (!window.PublicKeyCredential) {
        passkeyLoginButton.disabled = true;
        passkeyLoginButton.textContent = 'Passkeys not supported in this browser';
        return;
    }

    passkeyLoginButton.addEventListener('click', async function() {
        try {
            passkeyLoginButton.disabled = true;
            passkeyLoginButton.innerHTML = '<span class="inline-block animate-spin mr-2">⏳</span> Authenticating...';

            // Step 1: Get authentication options from server
            const beginResponse = await fetch('/passkey-auth/begin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
            });

            if (!beginResponse.ok) {
                throw new Error('Failed to begin authentication');
            }

            const { options } = await beginResponse.json();

            // Convert base64url strings to ArrayBuffers
            const publicKeyCredentialRequestOptions = {
                ...options,
                challenge: base64urlToBuffer(options.challenge),
                allowCredentials: options.allowCredentials.map(cred => ({
                    ...cred,
                    id: base64urlToBuffer(cred.id),
                })),
            };

            // Step 2: Prompt user with browser's WebAuthn UI
            const credential = await navigator.credentials.get({
                publicKey: publicKeyCredentialRequestOptions,
            });

            if (!credential) {
                throw new Error('No credential returned');
            }

            // Step 3: Send credential to server for verification
            const completeResponse = await fetch('/passkey-auth/complete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    id: credential.id,
                    rawId: bufferToBase64url(credential.rawId),
                    response: {
                        clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
                        authenticatorData: bufferToBase64url(credential.response.authenticatorData),
                        signature: bufferToBase64url(credential.response.signature),
                        userHandle: credential.response.userHandle ? bufferToBase64url(credential.response.userHandle) : null,
                    },
                    type: credential.type,
                }),
            });

            const result = await completeResponse.json();

            if (result.success) {
                window.location.href = result.redirect_url;
            } else {
                throw new Error(result.error || 'Authentication failed');
            }

        } catch (error) {
            console.error('Passkey authentication error:', error);
            alert('Failed to authenticate with passkey: ' + error.message);
            passkeyLoginButton.disabled = false;
            passkeyLoginButton.innerHTML = `
                <svg class="w-5 h-5 mr-2 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"></path>
                </svg>
                Sign in with passkey
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
