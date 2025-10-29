import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from openai import OpenAI

from core.models.this_server_configuration import ThisServerConfiguration

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def estimation_item_enhance_description_view(request: HttpRequest) -> JsonResponse:
    """
    Enhance an estimation item description using ChatGPT API.
    Expects a JSON payload with 'description' as the current description text.
    Returns enhanced description or error message.
    """
    try:
        logger.info(f"Enhance description request received from user: {request.user.username}")
        data = json.loads(request.body)
        current_description = data.get('description', '').strip()

        if not current_description:
            logger.warning("No description provided in enhance request")
            return JsonResponse({
                'success': False,
                'error': 'No description provided. Please enter some text first.'
            }, status=400)

        # Get ChatGPT API key from server configuration
        config = ThisServerConfiguration.current()
        api_key = config.chatgpt_api_key_decrypted if config else None

        if not api_key:
            logger.warning("ChatGPT API key not configured")
            return JsonResponse({
                'success': False,
                'error': 'ChatGPT API key is not configured. Please contact your administrator to configure it in the server settings.'
            }, status=400)

        # Call OpenAI API to enhance the description
        logger.info(f"Calling OpenAI API to enhance description (length: {len(current_description)} chars)")

        client = OpenAI(api_key=api_key)

        prompt = f"""You are a technical project estimation expert. Improve the following estimation item description by:

1. Making it more clear and specific
2. Breaking down the work into logical components if appropriate
3. Identifying potential technical challenges or dependencies
4. Adding relevant technical details that might be missing
5. Ensuring it's well-structured with markdown formatting (headers, bullet points, etc.)
6. Keeping it concise but comprehensive

Current description:
{current_description}

Provide an enhanced version that would help developers better understand the scope and requirements of this estimation item."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a technical project estimation expert who helps improve estimation item descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        enhanced_description = response.choices[0].message.content.strip()

        logger.info(f"Successfully enhanced description (new length: {len(enhanced_description)} chars)")

        return JsonResponse({
            'success': True,
            'enhanced_description': enhanced_description
        })

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error enhancing description: {e}", exc_info=True)
        error_message = str(e)
        # Provide more user-friendly error messages for common issues
        if 'authentication' in error_message.lower() or 'api key' in error_message.lower():
            error_message = 'Invalid API key. Please check the ChatGPT API key configuration.'
        elif 'rate limit' in error_message.lower():
            error_message = 'Rate limit exceeded. Please try again in a few moments.'
        elif 'timeout' in error_message.lower():
            error_message = 'Request timed out. Please try again.'
        else:
            error_message = f'An error occurred while enhancing the description: {error_message}'

        return JsonResponse({
            'success': False,
            'error': error_message
        }, status=500)
