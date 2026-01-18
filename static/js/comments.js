/**
 * Comments Section - AJAX handling for comments
 */
(function() {
    'use strict';

    const commentsSection = document.getElementById('comments-section');
    if (!commentsSection) return;

    const configElement = document.getElementById('comments-config');
    if (!configElement) return;

    const config = JSON.parse(configElement.textContent);
    const form = document.getElementById('comment-form');
    const contentInput = document.getElementById('comment-content');
    const internalCheckbox = document.getElementById('comment-internal');
    const submitBtn = document.getElementById('comment-submit-btn');
    const loadingSpinner = document.getElementById('comment-loading');
    const commentsList = document.getElementById('comments-list');
    const commentsCount = document.getElementById('comments-count');
    const noCommentsMessage = document.getElementById('no-comments-message');

    // Preview toggle elements
    const writeTab = document.getElementById('write-tab');
    const previewTab = document.getElementById('preview-tab');
    const writePanel = document.getElementById('write-panel');
    const previewPanel = document.getElementById('preview-panel');
    const previewContent = document.getElementById('preview-content');

    function showWriteMode() {
        writeTab.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
        writeTab.classList.remove('text-gray-500');
        previewTab.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
        previewTab.classList.add('text-gray-500');
        writePanel.classList.remove('hidden');
        previewPanel.classList.add('hidden');
    }

    function showPreviewMode() {
        previewTab.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
        previewTab.classList.remove('text-gray-500');
        writeTab.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
        writeTab.classList.add('text-gray-500');
        writePanel.classList.add('hidden');
        previewPanel.classList.remove('hidden');

        // Render markdown preview
        const content = contentInput.value.trim();
        if (content && typeof marked !== 'undefined') {
            previewContent.innerHTML = marked.parse(content);
        } else if (content) {
            previewContent.innerHTML = '<p>' + content.replace(/\n/g, '<br>') + '</p>';
        } else {
            previewContent.innerHTML = '<p class="text-gray-400 italic">Nothing to preview</p>';
        }
    }

    function getCsrfToken() {
        // First try to get from form input
        const formToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (formToken) return formToken;

        // Then try cookie (check both common names)
        const cookies = document.cookie.split('; ');
        for (const cookie of cookies) {
            if (cookie.startsWith('csrftoken=')) {
                return cookie.split('=')[1];
            }
            if (cookie.startsWith('csrf_token=')) {
                return cookie.split('=')[1];
            }
        }
        return null;
    }

    function setLoading(loading) {
        submitBtn.disabled = loading;
        loadingSpinner.classList.toggle('hidden', !loading);
    }

    function updateCount(delta) {
        const current = parseInt(commentsCount.textContent, 10) || 0;
        commentsCount.textContent = current + delta;
    }

    function showError(message) {
        alert(message);
    }

    async function handleSubmit(event) {
        event.preventDefault();

        const content = contentInput.value.trim();
        if (!content) {
            contentInput.focus();
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(config.createUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({
                    content_type: config.contentType,
                    object_id: config.objectId,
                    content: content,
                    is_internal: internalCheckbox?.checked || false,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to add comment');
            }

            // Remove "no comments" message if present
            if (noCommentsMessage) {
                noCommentsMessage.remove();
            }

            // Insert new comment at the top
            commentsList.insertAdjacentHTML('afterbegin', data.html);

            // Clear form and switch back to write mode
            contentInput.value = '';
            if (internalCheckbox) {
                internalCheckbox.checked = false;
            }
            showWriteMode();

            // Update count
            updateCount(1);

            // Attach delete handler to new comment
            const newComment = commentsList.querySelector('.comment-item');
            attachDeleteHandler(newComment);

        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleDelete(commentId, commentElement) {
        if (!confirm('Are you sure you want to delete this comment?')) {
            return;
        }

        const deleteUrl = config.deleteUrlTemplate.replace('/0/', '/' + commentId + '/');

        try {
            const response = await fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                },
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to delete comment');
            }

            // Remove comment element
            commentElement.remove();

            // Update count
            updateCount(-1);

            // Show "no comments" message if list is empty
            if (commentsList.querySelectorAll('.comment-item').length === 0) {
                commentsList.innerHTML = `
                    <div id="no-comments-message" class="px-6 py-8 text-center text-gray-500">
                        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                        </svg>
                        <p class="mt-2">No comments yet</p>
                        <p class="text-sm">Be the first to add a comment.</p>
                    </div>
                `;
            }

        } catch (error) {
            showError(error.message);
        }
    }

    function attachDeleteHandler(commentElement) {
        const deleteBtn = commentElement.querySelector('.comment-delete-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function() {
                const commentId = this.dataset.commentId;
                handleDelete(commentId, commentElement);
            });
        }
    }

    // Initialize
    form.addEventListener('submit', handleSubmit);

    // Tab click handlers
    if (writeTab && previewTab) {
        writeTab.addEventListener('click', showWriteMode);
        previewTab.addEventListener('click', showPreviewMode);
    }

    // Attach delete handlers to existing comments
    commentsList.querySelectorAll('.comment-item').forEach(attachDeleteHandler);
})();
